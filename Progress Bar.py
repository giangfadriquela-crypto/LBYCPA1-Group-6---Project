def progressBar(finishedTasks, totalTasks):
    percentageTasks = (finishedTasks / totalTasks) * 100 
    Bar = '|' + '█' * int(percentageTasks/2) + '-' * int((100 - percentageTasks)/2) + '|'
    return f'Percentage: {percentageTasks}%\n{Bar}'

print(progressBar(70, 100))