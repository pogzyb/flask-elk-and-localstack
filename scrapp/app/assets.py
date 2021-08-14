from flask_assets import Environment, Bundle, Filter


class ConcatHelper(Filter):

    def concat(self, out, hunks, **kw):
        out.write(';'.join(hunk.data() for hunk, _ in hunks))


css = Bundle(
    # 'node_modules/bootstrap/dist/css/bootstrap.css',
    # 'node_modules/font-awesome/css/font-awesome.css',
    'css/starter.css',
    # filters=('cssmin', 'cssrewrite'),
    output='gen/packed.css'
)


js = Bundle(
    # 'node_modules/jquery/dist/jquery.js',
    # 'node_modules/jquery-pjax/jquery.pjax.js',
    # 'node_modules/bootbox/dist/bootbox.min.js',
    # 'node_modules/bootstrap/dist/js/bootstrap.min.js',
    'js/home.js',
    'js/poll.js',
    'js/table.js',
    filters=(ConcatHelper,), #, 'jsmin'),
    output='gen/packed.js'
)


assets = Environment()
assets.register('css_all', css)
assets.register('js_all', js)
