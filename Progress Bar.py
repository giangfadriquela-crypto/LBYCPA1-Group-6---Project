def progressBar(finishedTasks, totalTasks):
    percentageTasks = (finishedTasks / totalTasks) * 100 
    Bar = '|' + '█' * int(percentageTasks/2) + '-' * int((100 - percentageTasks)/2) + '|'
    return f'Percentage: {percentageTasks}%\n{Bar}'

test_value1 = 67
test_value2 = 420
print(progressBar(test_value1, test_value2))
