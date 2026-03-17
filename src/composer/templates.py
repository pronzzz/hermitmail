import os
from jinja2 import Environment, FileSystemLoader

try:
    import markdown
except ImportError:
    pass

class NewsletterComposer:
    def __init__(self, templates_dir: str = "src/templates"):
        self.templates_dir = templates_dir
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
            
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
        
    def generate_html(self, issue_date: str, groups: dict, intro: str = "") -> str:
        """
        Generates the static HTML newsletter.
        """
        template = self.env.get_template('issue.html')
        return template.render(
            issue_date=issue_date,
            groups=groups,
            intro=intro
        )
        
    def generate_markdown(self, issue_date: str, groups: dict, intro: str = "") -> str:
        """
        Generates a Markdown version of the newsletter.
        """
        lines = []
        lines.append(f"# HermitMail Issue: {issue_date}")
        if intro:
            lines.append(f"\n{intro}\n")
            
        for heading, articles in groups.items():
            lines.append(f"\n## {heading}\n")
            for article in articles:
                lines.append(f"### [{article.get('title', 'Unknown Title')}]({article.get('url', '#')})")
                if article.get('author'):
                    lines.append(f"**By:** {article['author']}  ")
                if article.get('summary'):
                    lines.append(f"> {article['summary']}\n")
                lines.append("\n---\n")
                
        return "\n".join(lines)
