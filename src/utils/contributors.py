import re


class Contributors:
    def pull():
        with open(r'readme.md', 'r') as fp:
            r = fp.read()

        m = re.compile(r'%s.*?%s' % (">", "---"), re.S)
        contributors = m.search(r).group(0)
        return (contributors[2:-3])
