from tests.base import BaseTestCase
from nose.plugins.attrib import attr

import graphene


@attr('graphene')
class DbTest(BaseTestCase):

    def test_define_simple_schema(self):
        """ Simple graphene schema """

        class Query(graphene.ObjectType):
            hello = graphene.String(
                name=graphene.String(default_value='stranger')
            )

            def resolve_hello(self, info, name):
                return 'Hello {}'.format(name)


        schema = graphene.Schema(query=Query)

        graphql = '{ hello }'
        result = schema.execute(graphql)

