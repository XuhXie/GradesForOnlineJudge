import pandas as pd


class FileTypeError(TypeError):
    pass


class ContestScore:
    # for eval(cur_info) in gen_max_cases_
    global null
    null = ''

    def __init__(self, ):
        self.rank_path = ''
        self.submission_path = ''
        self.problem_path = ''
        self.ranks_df = None
        self.submission_df = None
        self.problem_df = None
        self.problem_names = []
        self.problem_ids = []
        self.contest_score = None

        # for calculate max cases
        self.target_problem = 0
        self.gen_all_cases = True

    def load_data(self, rank_path, submission_path, problem_path):
        # load data
        self.ranks_df = ContestScore.read_dataframe(rank_path)
        self.submission_df = ContestScore.read_dataframe(submission_path)
        self.rank_path = rank_path
        self.submission_path = submission_path

        # get problem_names and problem_ids
        self.get_problems(problem_path)

        rank_columns = self.ranks_df.columns.tolist()
        self.problem_names = rank_columns[6:]

        # process ranks
        drop_data = ['User ID', 'Real Name', 'Total Submission'] + self.problem_names
        self.contest_score = self.ranks_df.drop(axis=1, columns=drop_data)
        # calculate max cases
        self.contest_score['通过用例数'] = self.contest_score.apply(self.gen_max_cases, axis=1)
        # calculate max cases for certain problems
        self.gen_all_cases = False
        for index, p_id in enumerate(self.problem_ids):
            self.target_problem = p_id
            p_name = self.problem_names[index]
            self.contest_score[p_name] = self.contest_score.apply(self.gen_max_cases_problem, axis=1)
        # sort scores
        self.sort()

    def get_problems(self, problem_path):
        self.problem_df = ContestScore.read_dataframe(problem_path)
        self.problem_names = self.problem_df.title.to_list()
        self.problem_ids = self.problem_df.id.to_list()
        self.problem_path = problem_path

    def gen_max_cases(self, df):
        self.gen_all_cases = True
        return self.gen_max_cases_(df)

    def gen_max_cases_problem(self, df):
        self.gen_all_cases = False
        return self.gen_max_cases_(df)

    def gen_max_cases_(self, df):
        cur_max_cases = {}
        for i in range(len(self.submission_df)):
            if str(self.submission_df.iloc[i]['username']) == str(df['Username']) \
                    and (self.gen_all_cases or self.target_problem == self.submission_df.iloc[i]['problem_id']):
                try:
                    cur_info = self.submission_df.iloc[i]['info']
                    cur_problem_id = self.submission_df.iloc[i]['problem_id']
                    cur_score = sum(list(map(lambda x: x['result'] == 0, eval(cur_info)['data'])))

                    if not (cur_problem_id in cur_max_cases.keys()):
                        cur_max_cases[cur_problem_id] = cur_score
                    elif cur_score > cur_max_cases[cur_problem_id]:
                        cur_max_cases[cur_problem_id] = cur_score
                except:
                    continue
        return sum(cur_max_cases.values())

    def sort(self, by=['AC', '通过用例数', 'Total Time'], ascending=[False, False, True]):
        self.contest_score = self.contest_score.sort_values(by=by, ascending=ascending)
        return self.contest_score

    def save(self, path):
        self.contest_score.to_excel(path, index=False)
        return f"File Saved at {path} as Excel"

    @staticmethod
    def read_dataframe(path):
        filetype = path.split('.')[-1]
        dataframe = None
        if filetype == 'csv':
            dataframe = pd.read_csv(path)
        elif filetype == 'xlsx':
            dataframe = pd.read_excel(path)
        else:
            FileTypeError(filetype)
        return dataframe


test = ContestScore()
test.load_data(rank_path='./Contest-Rank.xlsx', submission_path='./Contest_submission.csv', problem_path='./problem.csv')
test.contest_score.head()
test.save('Result.xlsx')
