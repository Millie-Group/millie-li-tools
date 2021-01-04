from utils import *
from ResultsObject import ResultsObject
import re


class SearchResults(ResultsObject):
    """Linkedin User Profile Object"""

    attributes = ['personal_info', 'experiences',
                  'skills', 'accomplishments', 'interests']

    @property
    def results(self):
        results = {}

        users = all_or_default(self.soup, '.search-result__wrapper')

    @property
    def experiences(self):
        """
        Returns:
            dict of person's professional experiences.  These include:
                - Jobs
                - Education
                - Volunteer Experiences
        """
        experiences = {}
        container = one_or_default(self.soup, '.background-section')

        jobs = all_or_default(
            container, '#experience-section ul .pv-position-entity')
        jobs = list(map(get_job_info, jobs))
        jobs = flatten_list(jobs)

        experiences['jobs'] = jobs

        schools = all_or_default(
            container, '#education-section .pv-education-entity')
        schools = list(map(get_school_info, schools))
        experiences['education'] = schools

        volunteering = all_or_default(
            container, '.pv-profile-section.volunteering-section .pv-volunteering-entity')
        volunteering = list(map(get_volunteer_info, volunteering))
        experiences['volunteering'] = volunteering

        return experiences

    def to_dict(self):
        info = super(SearchResults, self).to_dict()
        info['personal_info']['current_company_link'] = ''
        jobs = info['experiences']['jobs']
        if jobs and jobs[0]['date_range'] and 'present' in jobs[0]['date_range'].lower():
            info['personal_info']['current_company_link'] = jobs[0]['li_company_url']
        else:
            print("Unable to determine current company...continuing")
        return info
