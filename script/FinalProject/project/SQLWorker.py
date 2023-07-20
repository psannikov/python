import sqlite3
import pandas as pd

class SQLWorker:

    TOP_SKILL_IN_ALL_VACANCY = 'top10all.xlsx'
    TOP_SKILL_IN_VACANCY_BY_INDUSTRY_ID = 'top10industry.xlsx'
    TOP_SKILL_IN_VACANCY_FILTER_COMPANIES = 'top10okved.xlsx'

    def __init__(self):
        self.df_skills_in_all = pd.DataFrame()
        self.df_skills_in_industries = pd.DataFrame()
        self.df_skills_in_companies = pd.DataFrame()

    def get_data_from_db_to_pd(self):
        connection = sqlite3.connect('airflow.db')
        select_all = """
        select s.skill,count(1) counts
        from vacancies v
        join skills s on v.id=s.id_vacancy
        group by s.skill
        order by count(1) desc
        limit 10
        """
        select_by_industries = """
        select skill,count(1) counts
        from vacancies v
        join skills s on v.id=s.id_vacancy
        where exists
        (select 1 from companies_industries i
        where i.industry_id like '9%'
        and i.company_id=v.company_id)
        group by skill
        order by 2 desc
        limit 10
        """
        select_by_companies = """
        with t1 as
        (select trim(replace(replace(replace(replace(replace(name,'ООО',''),'ЗАО',''),'АО',''),'"',''),'ОБЩЕСТВО С ОГРАНИЧЕННОЙ ОТВЕТСТВЕННОСТЬЮ','')) name
        from companies),
        t2 as
        (select * from vacancies v
        where exists (select 1 from t1 where t1.name like '%'||upper(v.company_name)||'%'))
        select skill,count(1) count from t2
        join skills s on t2.id=s.id_vacancy
        group by skill
        order by 2 desc
        limit 10
        """

        self.df_skills_in_all = pd.read_sql(select_all, connection)
        self.df_skills_in_industries = pd.read_sql(select_by_industries, connection)
        self.df_skills_in_companies = pd.read_sql(select_by_companies, connection)

    def save_df_to_excel(self):
        self.df_skills_in_all.to_excel(self.TOP_SKILL_IN_ALL_VACANCY)
        self.df_skills_in_industries.to_excel(self.TOP_SKILL_IN_VACANCY_BY_INDUSTRY_ID)
        self.df_skills_in_companies.to_excel(self.TOP_SKILL_IN_VACANCY_FILTER_COMPANIES)
