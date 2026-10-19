"""Minimal OpenAI-compatible API client. SPDX-License-Identifier: MIT"""
import json
import time
import urllib.error
import urllib.parse
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError('API redirects are not followed')


def chat(base_url, key, model, messages, temperature=0, max_tokens=4096):
    parsed = urllib.parse.urlsplit(base_url)
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('API base URL must not contain credentials, query parameters or fragments')
    if parsed.scheme != 'https' and not (parsed.scheme == 'http' and parsed.hostname in ('localhost', '127.0.0.1', '::1')):
        raise ValueError('Use HTTPS, or a loopback URL for local inference')
    payload = json.dumps({'model': model, 'messages': messages, 'temperature': temperature,
                          'max_tokens': max_tokens}, ensure_ascii=False).encode()
    opener = urllib.request.build_opener(NoRedirect)
    for attempt in range(3):
        request = urllib.request.Request(base_url.rstrip('/') + '/chat/completions', data=payload,
                    headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
        try:
            with opener.open(request, timeout=180) as response:
                result = json.load(response)
            answer = result['choices'][0]['message']['content']
            if not isinstance(answer, str) or not answer.strip():
                raise ValueError('API returned empty/non-text content')
            return answer
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise RuntimeError(f'API request failed (HTTP {exc.code}); response body withheld') from None
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise RuntimeError('API connection failed after 3 attempts') from None
        time.sleep(2 ** attempt)


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    temporary.replace(path)
