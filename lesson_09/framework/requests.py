class GetRequest:
    @staticmethod
    def get_params(environ: dict) -> dict:
        result = {}
        data = environ['QUERY_STRING']
        if data:
            params = data.split('&')
            for item in params:
                key, value = item.split('=')
                if key in result:
                    result[key].append(value)
                else:
                    result[key] = [value]
        return result


class PostRequest:
    @staticmethod
    def get_data(environ: dict) -> bytes:
        content_length = environ.get('CONTENT_LENGTH')
        content_length = int(content_length) if content_length else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    @staticmethod
    def get_params(environ: dict) -> dict:
        result = {}
        data = PostRequest.get_data(environ)
        if data:
            data = data.decode(encoding='utf-8')
            params = data.split('&')
            for item in params:
                key, value = item.split('=')
                result[key] = value
        return result
