from flask_assets import Environment, Bundle, Filter


class ConcatHelper(Filter):

    def concat(self, out, hunks, **kw):
        out.write(';'.join(hunk.data() for hunk, _ in hunks))


css = Bundle()

js = Bundle()
