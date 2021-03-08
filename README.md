# GradesForOnlineJudge
Grades Statistics for Online Judge
[原始的OJ开源项目地址](https://github.com/QingdaoU/OnlineJudgeFE)


需要三个文件

第一个是 contest_rank 在oj网页上下载

另外连个需要在数据库上导出，分别是 这次Contest的提交记录（submission 表）和这次Contest的题目信息（problem 表），注意要事先过滤掉其他contest的信息。

```python
test = ContestScore()

# load data and calculate scores , ranks automatically
test.load_data(rank_path='./Contest-Rank.xlsx', submission_path='./Contest_submission.csv', problem_path='./problem.csv')

# retun the result by a pandas DataFrame
test.contest_score

# Save result as excel
test.save('Result.xlsx')

```

如果没有problem表，可以用 set_problems 手动设置问题名和对应id

```python

test.set_problems([name1, name2, ...], [id1, id2, ...])
test.calculate()  # calculate result manually
test.sort() # default setting  sort(by=['AC', '通过用例数', 'Total Time'], ascending=[False, False, True])
test.save('Result.xlsx') 

```
