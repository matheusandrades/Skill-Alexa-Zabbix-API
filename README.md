# Skill-Alexa-Zabbix-API

No codigo lambda_fuction.py temos um exemplo para trabalhar em cima de API para obter valores atraves da Alexa, lembrando que é preciso tambem criar os Intents na plataforma e definidir as frases de gatilho para acionar as ações.
Tomem bastante cuidado com espaçamento na hora da construção do codigo.
Lembrando que este codigo é somente como fins demonstrativos para realizar a construções de chamadas API dentro da Alexa, para receber Alertas no Zabbix basta seguir o proximo topico.


# Alertas via Webhook

Dentro da pasta Alertas via WebHook, contem um arquivo em xml que basta você importa no seu zabbix e instalar a skill notify me na sua alexa para utilizar, lembrando que para instalar é necessario migrar sua conta amazon para EUA, depois basta voltar para Brasil que funcionara tudo corretamente.


## INFORMAÇÃO IMPORTANTE

Para apenas receber alertas do Zabbix na sua Alexa, basta importa o arquivo no Media Type no seu Zabbix e adicionar sua API KEY que você receber no email depois de ter instalado a Skill (Notify Me) na sua Alexa.
