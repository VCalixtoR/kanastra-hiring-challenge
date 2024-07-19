# FAST-API

<h3 align="center">
  API de processamento de boletos
</h3>


<p align="center">
  <a href="#-sobre-o-projeto">Sobre o projeto</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-resultados">Funcionamento</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-cenário-real">Cenário real</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-build-na-cloud-para-dev-e-prod">Build na Cloud para DEV e PROD</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-execução-local">Execução local</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#-como-contribuir">Como contribuir</a>&nbsp;&nbsp;&nbsp;
</p>

## 💇🏻‍♂️ Sobre o projeto

Este repositorio possui uma solução para uma entrevista da Kanastra incompleta mas que possui uma solução bem arquitetada, meu objetivo é, além de usar para a entrevista, utilizar esta arquitetura para criar um boilerplate com as boas práticas que fui conhecendo ao longo da minha carreira para a comunidade.

A tarefa é dedicada ao processamento de um arquivo csv que quando enviado via request, é processado pela API (Uso de FastAPI) para a geração de boletos com base em seus dados seguido pelo envio por email do resultado a cada usuários

## 💡 Resultados

Conforme citado anteriormente, a solução que entreguei a tempo foi mais focada na arquitetura ao invés da funcionalidade da API, infelizmente eu não tive o tempo para finalizar a solução, mas listo aqui, resumidamente, os pontos importantes que trouxe para mostrar minhas qualidades:

- **Módulos da arquitetura que favorece o principio de responsabilidade unica**: A arquitetura em módulos foi pensada para separar bem cada componente da arquitetura.
- **ORM com SQLAlchemy para abstração da base de dados**: O uso do ORM que permite o mapeamento de estruturas em python para modelos das bases de dados permite operações CRUD facilitadas na API além de facilitar a migração de diferentes bases de dados quando necessário. Nesta solução por exemplo, localmente é possível usar sqlite já em dev ou prod pode ser usado Postgres, MySQL do Cloud SQL da GCP ou RDS da AWS, para isso, basta apenas mudar a URL de conexão e todas as tabelas e sintaxe são mapeadas para o modelo da nova base pelo SQLAlchemy.
- **Providers criados com inversão de dependencia e injetados nos trechos necessários**: Favorece o desacoplamento e reuso facilitado dos providers, além de evitar side efects de mudanças internas das classes que implementam as interfaces, verifique /providers/app_injector.py para ver o container de injeção que é reutilizado para isto.
- **Logs são bem estruturados e com a inversão de dependencia**: Possível modifica-los sem precisar alterar o código que os chamam (Exemplo: Se for necessário colocar logs do grafana, basta alterar a linha `self.operation_logger = self.custom_uvicorn_logger.get_logger(IServicesEnum.PROCESS_FILE, self.operation_logger_id)` para retornar um operation_logger que é uma instância de uma classe que implementa a interface da inversão e que tenha os metodos .info, .warn, etc que enviam os dados para o Grafana ou outra ferramenta de monitoramento).
- **Docker e Docker-compose**: É montado um container docker simples mas bem pensado para evitar recarregamentos das layers do docker-compose após atualizações (Verifique o Dockerfile). O Dockercompose é mais pensado para a execução facilitada localmente.
- **Subida pra cloud**: Esta versão possui integração com a minha cloud para versionar a API em um Cloud Run da GCP usando CI CD (Verifique o cloudbuild.yaml), isso permite escalabilidade horizontal, o que apenas o uso de threads alvo desta tarefa não proporciona.
- **Autenticações**: Neste exemplo apenas por api key e basic, embora não sejam seguras, são bons exemplos de como aplicar a autenticação, no cenário real o mínimo deveria ser por JWT, OAuth ou outros.
- **Documentação automatica**: A rota autenticada com basic /docs cria uma documentação swagger automatica, tem como associar os modelos de respostas em formatos específicos para melhorar mais os retornos esperados em termos de modelo de dados e status.

## 💡 Cenário real

O que eu iria propor em um cenário real de produção?

Este cenário de emissão de boletos não deve ser feito em uma API, o cenário ideal envolveria uma arquitetura de recursos Cloud (Ex: Serverless com API Gateway, SQS, Lambdas e SES na AWS, Terraform, Pub Sub, Cloud functions e SendGrid na GCP). 

SQS e Pub Sub podem ser utilzados para fazer repetições em caso de falhas, e em cenários de automação de dados já populados em uma base, o ideal era o uso de eventos do AWS CloudWatch ou GCP Cloud Scheduler para a execução dessas etapas de forma automática e periódica.

Contudo com essa complexidade, seria interessante um framework de IaC para integrar nos pipelines CI CD para deploys automaticos da infraestrutura, por isso coloquei também Serverless e Terraform como recursos principais dos quais tenho esperiência e gosto de trabalhar.

## 📜 Build na Cloud para DEV e PROD

Esta solução usa de CI CD para subir esta aplicação para um Cloud Run da GCP através de commits para a master ou development (Atualmente criei apenas a branch master). Pontos de melhoria:
- Aplicar linting
- Aplicar testes
- Aplicar commits semanticos
- Se a infraestrutura for complexa, usar IaC com Terraform, Serverless ou outros

## 💻 Execução local

Para executar localmente:
- Verifique se o docker e docker-compose estao funcionais na sua maquina
- Crie um .env com base no .env.example (Para agilidade apenas copie o arquivo e renomeie)
- Execute `docker-compose up` (A base de dados será criada com os modelos ORMs no caso do Sqlite)

## 🤔 Como contribuir

Para contribuir:
- Faça uma branch a partir da development com o nome adequada à atividade:
  - ```feature/add-endpoint```
- Faça os commits/push para a branch.
- Faça um PR (Pull Request) para a branch development/master.
- Após seu PR ser aprovado, faça o merge e verifique se o deploy do GitHub Actions/CloudBuild não apresenta erros.