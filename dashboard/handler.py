import tornado.ioloop
import tornado.web
import tornado.websocket
from concurrent.futures import ThreadPoolExecutor
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class HTTPHandler(tornado.web.RequestHandler):
    '''Just a default handler'''

    executor = ThreadPoolExecutor(16)

    def initialize(self, *args, **kwargs):
        '''Initialize the server competition registry handler

        This handler is responsible for managing competition
        registration.

        Arguments:
            competitions {dict} -- a reference to the server's dictionary of competitions
        '''
        super(HTTPHandler, self).initialize(*args, **kwargs)

    def render_template(self, template, **kwargs):
        if hasattr(self, 'template_dirs'):
            template_dirs = self.template_dirs
        else:
            template_dirs = []

        if self.settings.get('template_path', ''):
            template_dirs.append(
                self.settings["template_path"]
            )
        env = Environment(loader=FileSystemLoader(template_dirs))

        try:
            template = env.get_template(self.template)
        except TemplateNotFound:
            raise TemplateNotFound(self.template)

        kwargs['current_user'] = self.current_user.decode('utf-8') if self.current_user else ''
        content = template.render(**kwargs)
        return content

    def set_default_headers(self, *args, **kwargs):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.set_header("Content-Security-Policy", "frame-ancestors 'self' localhost:* ")


class HTMLHandler(HTTPHandler):
    def initialize(self, template=None, template_kwargs=None, **kwargs):
        super(HTMLHandler, self).initialize()
        self.template = template
        self.baseurl = kwargs.get('baseurl', '/')
        self.template_kwargs = template_kwargs or {}

    def get(self, *args):
        '''Get the login page'''
        self.template_kwargs['baseurl'] = self.baseurl

        if not self.template:
            self.redirect(self.baseurl)
        else:
            if self.request.path == self.baseurl + 'logout':
                self.clear_cookie("user")
            template = self.render_template(self.template, **self.template_kwargs)
            self.write(template)
