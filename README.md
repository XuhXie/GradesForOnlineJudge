# GradesForOnlineJudge
Grades Statistics for Online Judge



需要三个文件

第一个是 contest_rank 在oj网页上下载

另外连个需要在数据库上导出，分别是 这次Contest的提交记录（submission 表）和这次Contest的题目信息（problem 表），注意要事先过滤掉其他contest的信息。

```python
test = ContestScore()

# load data and process data
test.load_data(rank_path='./Contest-Rank.xlsx', submission_path='./Contest_submission.csv', problem_path='./problem.csv')
# retun a pandas DataFrame
test.contest_score
# Save as excel
test.save('Result.xlsx')
# sort results
test.sort(by=['AC', '通过用例数', 'Total Time'], ascending=[False, False, True])
```
如果没有problem表，可以用 set_problems 手动设置问题名和对应id

```python
test.set_problems([name1, name2, ...], [id1, id2, ...])
```
