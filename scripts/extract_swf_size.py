#!/usr/bin/env python3
"""
extract_swf_size.py

Usage examples:
  python extract_swf_size.py toys
  python extract_swf_size.py https://cdn-ar.mundogaturro.com/juego/assets/cassettes.swf --only-number

The script will try a HEAD request first and read the Content-Length header.
If absent, it will stream the file and sum the received bytes.
"""

import argparse
import sys

try:
    import requests
except Exception:
    requests = None


def get_content_length_requests(url, timeout=10):
    try:
        r = requests.head(url, allow_redirects=True, timeout=timeout)
        cl = r.headers.get('Content-Length') or r.headers.get('content-length')
        if cl and cl.isdigit():
            return int(cl)
    except Exception:
        pass
    return None


def measure_by_get_requests(url, timeout=20, headers=None, verify=True):
    try:
        r = requests.get(url, stream=True, timeout=timeout, headers=headers or {}, verify=verify)
        total = 0
        for chunk in r.iter_content(8192):
            if not chunk:
                continue
            total += len(chunk)
        return total
    except Exception:
        return None


def get_size(url, verbose=False):
    if requests is None:
        raise RuntimeError('The "requests" library is required. Install with: pip install requests')
    headers = {'User-Agent': 'extract_swf_size/1.0 (+https://github.com/)'}

    # Try HEAD first (verify=True)
    try:
        r = requests.head(url, headers=headers, allow_redirects=True, timeout=10, verify=True)
        cl = r.headers.get('Content-Length') or r.headers.get('content-length')
        if cl and cl.isdigit():
            if verbose:
                print(f'[verbose] HEAD returned Content-Length={cl}', file=sys.stderr)
            return int(cl)
    except requests.exceptions.SSLError as e:
        if verbose:
            print(f'[verbose] HEAD SSL error: {e} (will retry without verification)', file=sys.stderr)
        # fallthrough to retry with verify=False
    except Exception as e:
        if verbose:
            print(f'[verbose] HEAD attempt failed: {e}', file=sys.stderr)

    # Some servers disallow HEAD; try a GET to see if headers include Content-Length
    # Try GET to read headers (verify=True)
    try:
        if verbose:
            print(f'[verbose] Trying GET to read headers from {url}', file=sys.stderr)
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=15, stream=True, verify=True)
        cl = r.headers.get('Content-Length') or r.headers.get('content-length')
        if cl and cl.isdigit():
            try:
                r.close()
            except Exception:
                pass
            if verbose:
                print(f'[verbose] GET headers include Content-Length={cl}', file=sys.stderr)
            return int(cl)
    except requests.exceptions.SSLError as e:
        if verbose:
            print(f'[verbose] GET headers SSL error: {e} (will retry without verification)', file=sys.stderr)
        # will retry with verify=False
    except Exception as e:
        if verbose:
            print(f'[verbose] GET headers attempt failed: {e}', file=sys.stderr)
        # fallthrough to retries

    # If we reached here, try HEAD/GET with verify=False as a last resort
    tried_insecure = False
    try:
        # disable insecure warnings only if needed
        from requests.packages.urllib3.exceptions import InsecureRequestWarning
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    except Exception:
        pass
    try:
        if verbose:
            print(f'[verbose] Retrying HEAD with verify=False', file=sys.stderr)
        r = requests.head(url, headers=headers, allow_redirects=True, timeout=10, verify=False)
        cl = r.headers.get('Content-Length') or r.headers.get('content-length')
        if cl and cl.isdigit():
            if verbose:
                print(f'[verbose] Insecure HEAD returned Content-Length={cl}', file=sys.stderr)
            return int(cl)
    except Exception as e:
        if verbose:
            print(f'[verbose] Insecure HEAD failed: {e}', file=sys.stderr)
    try:
        if verbose:
            print(f'[verbose] Retrying GET headers with verify=False', file=sys.stderr)
        r = requests.get(url, headers=headers, allow_redirects=True, timeout=15, stream=True, verify=False)
        cl = r.headers.get('Content-Length') or r.headers.get('content-length')
        if cl and cl.isdigit():
            try:
                r.close()
            except Exception:
                pass
            if verbose:
                print(f'[verbose] Insecure GET headers include Content-Length={cl}', file=sys.stderr)
            return int(cl)
    except Exception as e:
        if verbose:
            print(f'[verbose] Insecure GET headers failed: {e}', file=sys.stderr)
    tried_insecure = True

    # Fallback to GET and measure by streaming
    if verbose:
        print('[verbose] Streaming download to measure bytes (first try verify=True)...', file=sys.stderr)
    measured = measure_by_get_requests(url, headers=headers, verify=True)
    if measured is not None:
        if verbose:
            print(f'[verbose] Stream measured {measured} bytes', file=sys.stderr)
        return measured

    # If streaming with verify=True failed, and we haven't yet tried insecure, try verify=False
    if not tried_insecure:
        if verbose:
            print('[verbose] Streaming download with verify=False as last resort...', file=sys.stderr)
        measured = measure_by_get_requests(url, headers=headers, verify=False)
        if measured is not None:
            if verbose:
                print(f'[verbose] Insecure stream measured {measured} bytes', file=sys.stderr)
            return measured

    return None


def build_url_from_name(name, template):
    if name.startswith('http://') or name.startswith('https://'):
        return name
    return template.format(name)


def parse_args():
    p = argparse.ArgumentParser(description='Extrae el tamaño (bytes) de un SWF en el CDN.')
    p.add_argument('name_or_url', help='Nombre del SWF (ej: toys) o URL completa')
    p.add_argument('--template', default='https://cdn-ar.mundogaturro.com/juego/assets/{}.swf',
                   help='Plantilla de URL con un placeholder {} para el nombre')
    p.add_argument('--pretty', action='store_true', help='Mostrar información detallada (URL, KB)')
    p.add_argument('--verbose', action='store_true', help='Mostrar información diagnóstica')
    return p.parse_args()


def main():
    args = parse_args()
    url = build_url_from_name(args.name_or_url, args.template)

    try:
        size = get_size(url, args.verbose)
    except RuntimeError as e:
        print(str(e), file=sys.stderr)
        sys.exit(2)

    if size is None:
        print(f'Error: no se pudo obtener el tamaño desde {url}', file=sys.stderr)
        sys.exit(3)
    # Por defecto imprimir sólo el número (para uso en scripts). Usar --pretty para salida legible.
    if args.pretty:
        kb = size / 1024.0
        print(f'URL: {url}')
        print(f'Size (bytes): {size}')
        print(f'Size (KB): {kb:.2f}')
    else:
        print(size)


if __name__ == '__main__':
    main()
