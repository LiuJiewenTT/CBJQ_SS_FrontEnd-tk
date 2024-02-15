class Builtin_ExInfo:
    edition_str = 'Not Built'
    build_timestamp = 'Never'

    def summary_str_multiline(self):
        retv = f'Edition: {self.edition_str}\nBuild Timestamp: {self.build_timestamp}\n'
        return retv

    def summary_str_singleline(self):
        retv = f'Build Info: {self.edition_str} [{self.build_timestamp}]'
        return retv
