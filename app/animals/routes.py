from flask_restplus import Api, Resource, fields

from . import animals_blueprint
from app.models import Animal


api = Api(
        animals_blueprint,
        version='1.0',
        title='Animals API',
        description='A simple Animals API',
        doc='/doc/',
)

animal_def = api.model('Animal', {
    'name': fields.String(required=True, description="The animal's name"),
    'family': fields.String(required=True, description="The animal's family name"),
})


@api.route('/<string:family>/<string:name>')
@api.doc(
        responses={404: 'The animal is not found'},
        params={'name': "The animal's name", 'family': "The animal's family name"}
)
class AnimalResource(Resource):
    @api.doc(description="Get the animal")
    @api.marshal_with(animal_def)
    def get(self, family, name):
        try:
            return Animal.get(family, name)
        except Animal.DoesNotExist:
            api.abort(404, "{} does not exist".format(name))

    @api.doc(description='Put the animal')
    @api.expect(animal_def, validate=True)
    @api.marshal_with(animal_def)
    def put(self, family, name):
        animal = Animal(family, name)
        animal.save()

        return animal


@api.route('/')
class AnimalListResource(Resource):
    @api.doc(description="Get the animals by your query")
    @api.marshal_list_with(animal_def)
    def get(self):
        parser = api.parser()
        parser.add_argument('name', type=str)
        parser.add_argument('family', type=str)

        args = parser.parse_args()
        name = args['name']
        family = args['family']

        if name is None and family is None:
            animals = Animal.scan()
        elif name is not None and family is None:
            animals = Animal.scan(Animal.name == name)
        elif name is None and family is not None:
            animals = Animal.scan(Animal.family == family)
        else:
            animals = [Animal.get(family, name)]

        return animals
