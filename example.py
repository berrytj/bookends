import json
from datetime import datetime, timedelta
from collections import defaultdict


logs = {
  '2014/01/01': """
    {"hour": 0, "user": "tberry"}\n{"hour": 0, "user": "tberry"}\n
    {"hour": 0, "user": "ksagar"}\n{"hour": 1, "user": "ksagar"}\n
    {"hour": 1, "user": "tberry"}\n{"hour": 2, "user": "tberry"}\n
  """,
  '2014/01/02': """
    {"hour": 0, "user": "ksagar"}\n{"hour": 1, "user": "tberry"}\n
    {"hour": 2, "user": "ksagar"}\n{"hour": 2, "user": "ksagar"}\n
    {"hour": 2, "user": "ksagar"}\n{"hour": 2, "user": "tberry"}\n
  """,
}
today = datetime.strptime('2014/01/03', '%Y/%m/%d')
days_of_logs = 2


def pythonic():
  event_counts_by_hour = defaultdict(int)
  for days_ago in range(1, days_of_logs + 1):
    date = today - timedelta(days=days_ago)
    raw_logs = logs[date.strftime('%Y/%m/%d')]
    split_logs = raw_logs.strip().split('\n')
    filtered_logs = [log for log in split_logs if log]
    loaded_logs = [json.loads(log) for log in filtered_logs]
    for log in loaded_logs:
      event_counts_by_hour[log['hour']] += 1
  return event_counts_by_hour

print pythonic()


from operator import itemgetter

from toolz import mapcat
from funcy import count_by

def functional():
  return count_by(itemgetter('hour'),
                  map(json.loads,
                      filter(None,
                             mapcat(lambda output: output.strip().split('\n'),
                                    map(lambda date: logs[date.strftime('%Y/%m/%d')],
                                        map(lambda days_ago: today - timedelta(days=days_ago),
                                            range(1, days_of_logs + 1)))))))

print functional()


from toolz.curried import map, filter, mapcat, curry
count_by = curry(count_by)

from bookends import _

def piped():
  return (_| range(1, days_of_logs + 1)
           | map(lambda days_ago: today - timedelta(days=days_ago))
           | map(lambda date: logs[date.strftime('%Y/%m/%d')])
           | mapcat(lambda output: output.strip().split('\n'))
           | filter(None)
           | map(json.loads)
           | count_by(itemgetter('hour'))
           |_)

print piped()

