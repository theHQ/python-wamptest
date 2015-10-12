FROM thehq/crossbar:0.11.1
MAINTAINER Eric Chapman <eric@thehq.io>

COPY wamptest/ /app/wamptest/
COPY tests/*.py /app/
COPY tests/run_test.sh /app/run_test.sh
RUN chmod +x /app/run_test.sh

ENTRYPOINT ["/app/run_test.sh"]