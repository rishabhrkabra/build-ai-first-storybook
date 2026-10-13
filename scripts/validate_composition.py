#!/usr/bin/env python3
"""Validate measured relationships; never claims to collect/render the UI."""
import json
import sys


def validate(data):
    errors = []
    checks = data.get('checks', [])
    if not checks:
        return ['No measured checks supplied']
    for i, c in enumerate(checks):
        key = c.get('id', f'check[{i}]')
        def fail(message):
            errors.append(f'{key}: {message}')
        if not c.get('subjects') or not c.get('source'):
            fail('Missing subjects or source evidence')
        kind = c.get('kind')
        try:
            if kind in ('card_row', 'action_row'):
                items = c['items']
                if len(items) < 2:
                    fail('Expected at least two peers')
                elif kind == 'card_row':
                    if not c.get('masonryApproved', False):
                        if max(x['height'] for x in items)-min(x['height'] for x in items) > 1:
                            fail('Unequal same-row card heights')
                        if max(x['footerY'] for x in items)-min(x['footerY'] for x in items) > 1:
                            fail('Misaligned card footers')
                else:
                    if not c.get('intentionalMixedSize', False) and max(x['height'] for x in items)-min(x['height'] for x in items) > 1:
                        fail('Undeclared mixed action sizes')
                    centres = [x['y']+x['height']/2 for x in items]
                    if max(centres)-min(centres) > 1:
                        fail('Misaligned action centres')
            elif kind == 'field_helper':
                if not c['sameFieldAncestor'] or c['controlGap'] >= c['nextFieldGap']:
                    fail('Helper ownership/proximity broken')
            elif kind == 'url_input':
                if c['urlOnly'] and not c['verifiedLinkIcon']:
                    fail('Missing project-required URL icon')
            elif kind == 'state_icon':
                if c['actualTokenId'] != c['expectedTokenId']:
                    fail('Wrong semantic foreground binding')
                if abs(c['actualStroke']-c['expectedStroke']) > .01:
                    fail('Wrong final icon stroke')
            elif kind == 'bounds':
                if c['horizontalOverflow'] or c['verticalOverflow'] or c['unintendedOverlap']:
                    fail('Overflow or unintended overlap')
            else:
                fail(f'Unsupported check kind: {kind}')
        except (KeyError, TypeError, ValueError) as exc:
            fail(f'Incomplete measurement: {exc}')
    return errors


if __name__ == '__main__':
    with open(sys.argv[1], encoding='utf-8') as f:
        payload = json.load(f)
    found = validate(payload)
    print(json.dumps({'checked': len(payload.get('checks', [])), 'errors': found}, indent=2))
    sys.exit(1 if found else 0)
