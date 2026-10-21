"""Deterministic review priorities derived from an existing studio result.

No network calls, generated answers, or automatic operational changes.
"""
import json
PROJECT = 'privacy-forge'
NAME = 'Privacy Forge'

def attach(request, result):
    lab = result['lab']
    items = []

    def add(key, severity, title, detail):
        items.append({'id': key, 'severity': severity, 'title': title, 'detail': detail})
    receipt = lab['receipt']
    for c in lab['columns']:
        if c['detected'] and c['action'] in {'keep', 'generalize'}:
            add('exposure-' + c['column'], 'high', c['column'] + ': retained signals', str(c['detected']) + ' detected cell(s) use ' + c['action'] + '. Inspect purpose and residual information manually.')
    if not receipt['quasi_identifiers']:
        add('qi', 'review', 'No quasi-identifiers selected', 'Group-size analysis has no selected dimensions. Consider combinations that could identify someone; selection alone does not certify privacy.')
    elif lab['singleton_groups']:
        add('singletons', 'high', str(lab['singleton_groups']) + ' singleton group(s)', 'Each selected group contains one record. Generalization and larger groups still do not guarantee anonymity.')
    add('tokens', 'info', 'Tokens are run-scoped pseudonyms', 'Token salts are random and not exported. Cross-run joins are not supported. The review report excludes source cell values and the token salt.')
    add('approval', 'review', 'Review the output before sharing', 'Heuristic discovery can miss identifiers. The review checklist is a workflow aid, not a compliance or anonymization certificate.')
    items.sort(key=lambda x: {'high': 0, 'review': 1, 'info': 2}[x['severity']])
    review = {'version': '2.1.0', 'project': PROJECT, 'name': NAME, 'items': items, 'summary': {level: sum((x['severity'] == level for x in items)) for level in ['high', 'review', 'info']}, 'scope': 'Deterministic review aid from this experiment. Checklist completion does not certify correctness, safety, production readiness, or privacy.'}
    report = '# ' + NAME + ' — review handoff\n\n' + review['scope'] + '\n\n'
    for item in items:
        title = item['title'].replace('\n', ' ').replace('\r', ' ')
        detail = item['detail'].replace('\n', ' ').replace('\r', ' ')
        report += '- [ ] [' + item['severity'].upper() + '] ' + title + '\n  ' + detail + '\n'
    result['review'] = review
    result['artifacts'] += [{'name': 'review-handoff.md', 'content': report}, {'name': 'review-priorities.json', 'content': json.dumps(review, indent=2)}]
    return result
