import requests
import json
import logging

class PullRequestProfile :
    '''
    This class instantiates the Sonarcloud Quality Profile for a Pull Request from one SCM branch to another.
    '''
    def __init__(self, url="https://sonarcloud.io", **kwargs):
        self.url = url
        self.authorization = kwargs.get("authorization")
        self.pullrequest = kwargs.get("pullrequest")
        self.projectkey = kwargs.get("projectkey")
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": self.authorization,
        }

    def gate_status(self):
        '''
        This method returns the quality gate status. 
        "0" is returned when the quality gate fails and '1' is returned when the quality gate passes. Both values are intergers.         
        '''
        url = self.url + "/api/qualitygates/project_status"
        headers = self.headers
        params = {"projectKey": self.projectkey , "pullRequest": self.pullrequest}
        resp = requests.get(url=url, headers=headers, params=params, auth=(self.authorization, ''))
        if resp.status_code != 200:
            raise Exception (':::: Response Code = {} ::::'.format(resp.status_code))
        else:
            data = []
            j = resp.json()
            s = j['projectStatus']['status']
            k = {"status": "{}".format(s)}
            data.append(k)
            default_value = 'N/A'
            for i in j['projectStatus']['conditions']:
                c = {
                "metric" : "{}".format(i.get('metricKey', default_value)),
                "threshold" : "{}".format(i.get('errorThreshold', default_value)),
                "value" : "{}".format(i.get('actualValue', default_value)),
                "operator" : "{}".format(i.get('comparator', default_value))
                }
                data.append(c)     
        return data 


    def measure(self, metric):
        '''
        This method returns the Measure of specified metric.
        Example of metric: coverage, code_smells, duplicated_lines_density, vulnerabilities 
        '''
        url = self.url + "/api/measures/component"
        headers = self.headers
        params = {"component": self.projectkey , "pullRequest": self.pullrequest, 'metricKeys': metric}
        resp = requests.get(url=url, headers=headers, params=params, auth=(self.authorization, ''))
        if resp.status_code != 200:
            raise Exception (':::: Response Code = {} ::::'.format(resp.status_code))
        else:
            data = resp.json()["component"]["measures"][0]["value"]
        return data

    def issues(self, status, page_size=100):
        '''
        This method returns issues with the specified status.
        Example of status: OPEN, CLOSED, CONFIRMED, RESOLVED, REOPENED 
        '''
        url = self.url + "/api/issues/search"
        headers = self.headers
        params = {"projects": self.projectkey , "pullRequest": self.pullrequest, 'statuses': status}
        resp = requests.get(url=url, headers=headers, params=params, auth=(self.authorization, ''))
        if resp.status_code != 200:
            raise Exception (':::: Response Code = {} ::::'.format(resp.status_code))
        else:
            t = resp.json()["total"]
            page_num = t//page_size
            page_num += 1
            data = []
            for i in range(1,page_num+1):
                params = {"projects": self.projectkey , "pullRequest": self.pullrequest, 'statuses': status, 'p': i, 'ps': page_size}
                resp = requests.get(url=url, headers=headers, params=params, auth=(self.authorization, ''))
                if resp.status_code != 200:
                    raise Exception (':::: Response Code = {} ::::'.format(resp.status_code))
                else:
                    s = resp.json()["issues"]
                    for j in s:
                        data.append(j)
        return data


    def issues_info(self, issues):
        '''
        This method returns issue details to be reported.
        '''
        default_value = 'N/A'
        data = []
        for i in issues:
            k = i.get('component')
            j = k.split(':')[-1]
            s = {'Associated Rule': '{}'.format(i.get('rule',default_value)), 'Component': '{}'.format(j), 'Message': '{}'.format(i.get('message',default_value)), 'Issue Type': '{}'.format(i.get('type', default_value)), 'Severity': '{}'.format(i.get('severity', default_value)), "Line": '{}'.format(i.get('line', default_value)), 'Estimated Effort': '{}'.format(i.get('effort', default_value)), 'Author': '{}'.format(i.get('author', default_value))}
            data.append(s)

        return data
