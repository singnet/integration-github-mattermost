FROM python:3.10-alpine AS builder

WORKDIR /mattermost

COPY ./requirements.txt .

RUN pip3 install -r ./requirements.txt -t .

FROM gcr.io/distroless/python3 as mattermost

COPY --from=builder /mattermost /mattermost

WORKDIR mattermost

COPY . .

ENTRYPOINT ["python3"]
CMD ["main.py"]
