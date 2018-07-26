
class SearchService:

    def __init__(self, *args, **kwargs):
        """
        Init service
        If any parameters are given to constructor, a delayed initializer is
        called with these parameters.
        """

        # es connection
        self.host = None
        self.port = None

        # index name
        self.index = None
        # document type
        self.doc_type = None

        if args or kwargs:
            self.init(*args, **kwargs)

    def init(
        self,
        host='localhost',
        port=9002,
        index_name=None,
        doc_type='content'):
        """
        Delayed service initializer. Called either by constructor if args
        passed in, or later in userland code to configure the service.

        :param host: str, elasticsearch host
        :param port: int, elasticsearch port
        :param index_name: str, index name
        :param doc_type: str, document type
        :return: shiftcontent.search_service.SearchService
        """
        self.host = host
        self.port = port
        self.index = index_name
        self.doc_type = doc_type

        return self



