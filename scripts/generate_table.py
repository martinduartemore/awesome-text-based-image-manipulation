import json
import re



def generate_table_papers():
    with open('./data/papers.json') as f:
        papers = json.load(f)
    papers = sorted(papers, key=lambda k: k['date'], reverse=True)

    header = ['|Date|Title|Venue|Citations|Paper|Code|']
    header.append(re.sub(r'(?<=\|).*?(?=\|)', ':---:', header[0]))

    paper_rows = []

    for paper in papers:
        paper_info = {}
        paper_info['date'] = paper['date']
        paper_info['title'] = paper['title']
        paper_info['venue'] = paper['venue']
        paper_info['citations'] = 'N/A'

        links = []
        for info in paper['paper_info']:
            info_str = '[{}]({})'.format(info['name'], info['link'])
            links.append(info_str)
        links = '<br>'.join(links)
        paper_info['links'] = links

        codes = []
        for code in paper['code']:
            if code['name'] == '-' and code['link'] == '-':
                continue
            code_str = '[{}]({})'.format(code['name'], code['link'])
            github_info = '/'.join(code['link'].split('/')[-2:])
            github_stars = ' ![](https://img.shields.io/github/stars/{}.svg?style=social)'
            github_stars = github_stars.format(github_info)
            code_str += '<br>' + github_stars
            codes.append(code_str)
        codes = '<br>'.join(codes)
        if codes == '':
            codes = '-'
        paper_info['codes'] = codes

        paper_row = '|{date}|{title}|{venue}|{citations}|{links}|{codes}|'.format(**paper_info)
        paper_rows.append(paper_row)

    return '\n'.join(header + paper_rows)



if __name__ == '__main__':
    with open('README_BASE.md', 'r') as f:
        readme = f.read()

    table_papers = generate_table_papers()
    readme = readme.replace('{{{table-papers}}}', table_papers)

    with open('README.md', 'w') as f:
        f.write(readme)
