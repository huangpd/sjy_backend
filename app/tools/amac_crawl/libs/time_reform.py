import pendulum

tz = "Asia/Shanghai"


def month_range(month_offset):
    month_range_list = [
        pendulum.now(tz).subtract(months=month_offset).start_of('month'),
        pendulum.now(tz).subtract(months=month_offset).end_of('month')
    ]
    return month_range_list


def get_last_months(months):
    return pendulum.now(tz).subtract(months=months).start_of('month'), pendulum.now(tz)


def timestamp2str(timestamp):
    return pendulum.from_timestamp(timestamp, tz=tz).to_date_string()
