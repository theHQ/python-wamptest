FROM erichq/crossbar
MAINTAINER Eric Chapman <eric@headquartershq.com>

COPY wamptest/ /app/wamptest/
COPY tests/*.py /app/
COPY tests/run_test.sh /app/run_test.sh
RUN chmod +x /app/run_test.sh

ENTRYPOINT ["/app/run_test.sh"]