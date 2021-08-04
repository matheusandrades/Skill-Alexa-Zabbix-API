# -*- coding: utf-8 -*-

# Este exemplo demonstra a manipulação de intents de uma habilidade do Alexa usando o Alexa Skills Kit SDK para Python.
# Visite https://alexa.design/cookbook para obter exemplos adicionais sobre a implementação de slots, gerenciamento de diálogo,
# persistência de sessão, chamadas de API e muito mais.
# Este exemplo é construído usando a abordagem de classes de manipulador no construtor de habilidades.
import logging
import ask_sdk_core.utils as ask_utils
import time
from zabbix_api import ZabbixAPI

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Seja bem vindo a sua primeira skill com o Zabbix, em que posso te ajudar?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class zabbixIntentHandler(AbstractRequestHandler):
    """Handler for Zabbix  Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("zabbixIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        zapi = ZabbixAPI(server="http://URL-SERV/zabbix")
        zapi.login("LOGIN", "SENHA")
         
        triggers = zapi.trigger.get ({
            "output": ["description", "lastchange"],
            "selectHosts": ["hostid", "host"],
            "selectLastEvent": ["eventid", "acknowledged", "objectid", "clock", "ns"],
            "sortfield" : "lastchange",
            "monitored": "true",
            "recent": "true",
            "limit": 1,
            "sortorder": "DESC",
            "only_true": "true",
            "maintenance":  "false",
            "expandDescription": True,
            "filter":{"value":1}
            })

            for y in triggers:
            nome_host = y["hosts"][0]["host"]
            idade = time.time() - float(y["lastchange"])
            pegadia = "{0.tm_yday}".format(time.gmtime(idade))
            dia = int(pegadia) - 1
            duracao = "dias {0.tm_hour} horas {0.tm_min} minutos".format(time.gmtime(idade))
            ultima_alteracao = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(float(y["lastchange"])))

        speak_output = str(y["description"]) + " no dia " + str(ultima_alteracao) + " e a duração do incidente é de " + str(duracao)

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask ("adicione um novo prompt se quiser manter a sessão aberta para que o usuário responda")
                .response
        )


class zabbixInfracaoHandler(AbstractRequestHandler):
    """Handler for Zabbix Infracao Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.zabbixInfracao")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        zapi = ZabbixAPI(server="http://URL-SERV/zabbix")
        zapi.login("LOGIN", "SENHA")
         
        host = zapi.item.get ({
            "output": "extend",
            "filter":{"host":["dgt-HL99"]},
            "search": {"key_": "infracoes-total"},
            "selectItems": "Quantidade de Infrações",
            "sortfield": "name"
            })

        for y in host:
            status = host[0]['lastvalue']
            ultima_alteracao = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(float(y["lastclock"])))

        speak_output = "O pardal HLO-99 registrou " + str(status) + " infrações e a última coléta foi " + str(ultima_alteracao)
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Xauzinho!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, não tenho certeza.. Você pode dizer Incidente ou Infração. O que você gostaria de fazer?"
        reprompt = "Não entendi. Em que posso ajudá-lo?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        #Qualquer lógica de limpeza vai aqui.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """O refletor de intenção é usado para teste e depuração do modelo de interação.
    Ele simplesmente repetirá a intenção que o usuário disse. Você pode criar manipuladores personalizados
    para suas intenções, definindo-as acima e, em seguida, adicionando-as à solicitação
    corrente do manipulador abaixo.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask ("adicione um novo prompt se quiser manter a sessão aberta para que o usuário responda")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Tratamento de erros genéricos para capturar qualquer sintaxe ou erros de roteamento. Se você receber um erro
    informando que a cadeia do manipulador de solicitação não foi encontrada, você não implementou um manipulador para
    a intenção sendo invocada ou incluída no construtor de habilidades abaixo.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Desculpe, tive problemas para fazer o que você pediu. Por favor, tente novamente."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(zabbixIntentHandler())
sb.add_request_handler(zabbixInfracaoIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
