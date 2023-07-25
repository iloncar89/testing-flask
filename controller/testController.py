from flask import Blueprint, jsonify, request, json
from dependency_injector.wiring import inject, Provide

from config.containers import Container
from service.testService import TestService
from domain.person import Person
from model.person import Person as PersonModel
from payload.schemas import PersonRequest, PersonResponse, GreetingRequest, GreetingResponse, CalculateFibonacciResponse
import utils.appConstants as Constants

blueprint = Blueprint('test_api', __name__)


@blueprint.route("/case1", methods=["GET"])
def hello():
    response= json.loads(GreetingResponse(greeting=Constants.HELLO).json())
    return jsonify(response)


@blueprint.route("/case2", methods=["POST"])
def greeting():
    request_data = request.get_json()
    greeting_request = GreetingRequest(name=request_data['name'])
    response = json.loads(GreetingResponse(greeting=Constants.HELLO + " " + greeting_request.name).json())
    return jsonify(response)


@blueprint.route("/case3/<int:number>", methods=["GET"])
@inject
def calculate_fibonacci(
        number: int,
        test_service: TestService = Provide[Container.test_service]):
    try:
        calculation_result = test_service.calculate_fibonacci(number)
        
        response = json.loads(CalculateFibonacciResponse(number=calculation_result).json())
        return jsonify(response)
    except InterruptedError:
        return Constants.ERROR, 500


@blueprint.route("/case4", methods=["POST"])
@inject
def create_get_delete_person_test_case(
        test_service: TestService = Provide[Container.test_service]):
    request_data = request.get_json()
    person_request = PersonRequest(first_name=request_data['first_name'], last_name=request_data['last_name'],
                                   year_of_birth=request_data['year_of_birth'])
    person = PersonModel(**person_request.dict())
    person = test_service.create_get_delete_person_test_case(person)
    person_response = json.loads(PersonResponse(id=person.id, first_name=person.first_name, last_name=person.last_name,
                                     year_of_birth=person.year_of_birth).json())
    return jsonify(person_response)


@blueprint.route("/case5", methods=["POST"])
@inject
def create_get_delete_person_orm_test_case(
        test_service: TestService = Provide[Container.test_service]):
    request_data = request.get_json()
    person_request = PersonRequest(first_name=request_data['first_name'], last_name=request_data['last_name'],
                                   year_of_birth=request_data['year_of_birth'])
    person = Person(**person_request.dict())
    person = test_service.create_get_delete_person_orm_test_case(person)
    person_response = json.loads(PersonResponse(id=person.id, first_name=person.first_name, last_name=person.last_name,
                                     year_of_birth=person.year_of_birth).json())
    return jsonify(person_response)
