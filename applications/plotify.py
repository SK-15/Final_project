import matplotlib.pyplot as plt

def logs_plot(type,logs):
    log_value = []
    log_time_stamp = []
    for log in logs:
        log_value.append(log.value)
        log_time_stamp.append(log.time_stamp)
    if type == '0':
        int_value = []
        for a in log_value:
            int_value.append(int(a))
        fig, ax = plt.subplots()
        ax.bar(log_time_stamp, int_value)
        fig.savefig('static/images/plot.png')
    else:
        fig, ax = plt.subplots()
        ax.plot(log_time_stamp, log_value)
        fig.savefig('static/images/plot.png')