import unittest

from make_website import *

class MakeWebsite_Test(unittest.TestCase):

    def test_surround_block(self):

        # test text with surrounding h1 tags
        self.assertEqual("<h1>Eagles</h1>", surround_block('h1', 'Eagles'))

        # test text with surrounding h2 tags
        self.assertEqual("<h2>Red Sox</h2>", surround_block('h2', 'Red Sox'))

        # test text with surrounding p tags
        self.assertEqual('<p>Lorem ipsum dolor sit amet, consectetur ' +
                         'adipiscing elit. Sed ac felis sit amet ante porta ' +
                         'hendrerit at at urna.</p>',
                         surround_block('p', 'Lorem ipsum dolor sit amet, consectetur ' +
                                        'adipiscing elit. Sed ac felis sit amet ante porta ' +
                                        'hendrerit at at urna.'))

    def test_create_email_link(self):

        # test email with @ sign
        self.assertEqual(
            '<a href="mailto:lbrandon@wharton.upenn.edu">lbrandon[aT]wharton.upenn.edu</a>',
            create_email_link('lbrandon@wharton.upenn.edu')
        )

        # test email with @ sign
        self.assertEqual(
            '<a href="mailto:krakowsky@outlook.com">krakowsky[aT]outlook.com</a>',
            create_email_link('krakowsky@outlook.com')
        )

        # test email without @ sign
        self.assertEqual(
            '<a href="mailto:lbrandon.at.seas.upenn.edu">lbrandon.at.seas.upenn.edu</a>',
            create_email_link('lbrandon.at.seas.upenn.edu')
        )

    def test_load_txt_file(self):

        #test that function accurately converts info in the text file to a list of strings
        self.assertEqual(['I.M. Student',
                         'Courses :- Programming Languages and Techniques, Biomedical image analysis, Software Engineering',
                         'Projects',
                         'CancerDetector.com, New Jersey, USA - Project manager, codified the assessment and mapped it to the CancerDetector ontology. Member of the UI design team, designed the portfolio builder UI and category search pages UI. Reviewed existing rank order and developed new search rank order approach.',
                         'Biomedical Imaging - Developed a semi-automatic image mosaic program based on SIFT algorithm (using Matlab)',
                          '------------------------------',
                          'tonyl@seas.upenn.edu'], load_txt_file('resume.txt'))

        #test other file from testResumes
        self.assertEqual(['brandon (name lowercase)', 'Courses :- Programming Languages and Techniques, Biomedical image analysis, Software Engineering',
                         'Projects', 'CancerDetector.com, New Jersey, USA - Project manager, codified the assessment and mapped it to the CancerDetector ontology. Member of the UI design team, designed the portfolio builder UI and category search pages UI. Reviewed existing rank order and developed new search rank order approach.',
                         'Biomedical Imaging - Developed a semi-automatic image mosaic program based on SIFT algorithm (using Matlab)', '------------------------------', 'lbrandon@wharton.upenn.edu'],
                         load_txt_file('TestResumes/resume_bad_name_lowercase/resume.txt'))


    def test_get_name(self):

        #test name
        self.assertEqual('Calleigh Winberg', get_name('Calleigh Winberg'))

        #test name with whitespace
        self.assertEqual('Calleigh Winberg', get_name('   Calleigh Winberg   '))

        #test invalid name
        self.assertEqual('Invalid Name', get_name('   calleigh Winberg'))

        #test name starting with number, edge case
        self.assertEqual('Invalid Name', get_name('1alleigh winberg   '))

        #ensure that a type string is returned
        self.assertEqual(type('Calleigh'), type(get_name('Calleigh')))


    def test_get_email(self):

        #test correct email
        self.assertEqual('tonyl@seas.upenn.edu', get_email(load_txt_file('resume.txt')))

        #test email not using load_txt_file
        self.assertEqual('tonyl@seas.upenn.edu', get_email(['tonyl@seas.upenn.edu']))

        #test invalid email
        self.assertEqual('', get_email(['tonyl1@seas.upenn.edu']))

        # test invalid email
        self.assertEqual('', get_email(['tonyl@seas.upenn.org']))


    def test_locate_line(self):

        #test to find student in resume.txt file
        self.assertEqual(0, locate_line((load_txt_file('resume.txt')), 'Student'))

        #test to find Courses
        self.assertEqual(1, locate_line((load_txt_file('resume.txt')), 'Courses'))

        #test to find 10 '-'
        self.assertEqual(5, locate_line((load_txt_file('resume.txt')), '----------'))

        #test edge case where there the identifier is not found in the txt file
        self.assertEqual(None, locate_line((load_txt_file('resume.txt')), '???'))




    def test_get_courses(self):

        #test the test resume.txt file
        self.assertEqual(['Programming Languages and Techniques', 'Biomedical image analysis',
                          'Software Engineering'], get_courses(load_txt_file('resume.txt')))

        #test when there's more weird punctuation
        self.assertListEqual(['Engineering', 'MCIT 5920', 'Learning'],
                             get_courses(['Name', 'Courses   :::---124.>>"?/     Engineering, MCIT 5920, Learning']))

        #test when 'Courses' isn't the first word and there's no weird punctuation. Also excessive whispace between courses
        self.assertListEqual(['One', 'Two', 'Three'],
                             get_courses(['Name', ' testing Courses     One     , Two,    Three   ']))


    def test_get_projects(self):

        #test basic resume.txt file
        self.assertEqual(['CancerDetector.com, New Jersey, USA - Project manager, codified the assessment and mapped '
                         'it to the CancerDetector ontology. Member of the UI design team, designed the portfolio '
                         'builder UI and category search pages UI. Reviewed existing rank order and developed new '
                         'search rank order approach.', 'Biomedical Imaging - Developed a semi-automatic image mosaic '
                                                        'program based on SIFT algorithm (using Matlab)'],
                         get_projects(load_txt_file('resume.txt')))

        #test that the len on the new list is the same as the old
        self.assertEqual(2, len(get_projects(load_txt_file('resume.txt'))))

        #test edge Projects line and more than 10 '-'
        self.assertEqual(['course 1', 'course 2'], get_projects(['Name', 'random line', '', '    Projects !@#$%^ . ',
                                                                 'course 1', 'course 2', '------------------    --']))



    def test_basic_info_section(self):

        #test basic info section when the input is given
        self.assertEqual(('<div>\n<h1>I.M. Student</h1>\n<p>Email: <a href="mailto:tonyl@seas.upenn.edu">tonyl[aT]seas.upenn.edu</a></p>'
                          '\n</div>'), basic_info_section('I.M. Student', 'tonyl@seas.upenn.edu'))


        #meant to just test the functionality of basic_info_section pulling a testResume file but it also test get_name and load_txt_file
        self.assertEqual(('<div>\n<h1>Invalid Name</h1>\n<p>Email: <a href="mailto:lbrandon@wharton.upenn.edu">lbrandon[aT]wharton.upenn.edu</a></p>'
                          '\n</div>'), basic_info_section(get_name(load_txt_file('TestResumes/resume_bad_name_lowercase/resume.txt')[0]),
                                                          get_email(load_txt_file('TestResumes/resume_bad_name_lowercase/resume.txt'))))


    def test_project_section(self):

        #test project section function
        self.assertEqual('<div>\n<h2>Projects</h2>\n<ul>\n<li>CancerDetector.com, New Jersey, USA - Project manager, codified the assessment and mapped it to the CancerDetector ontology. '
                         'Member of the UI design team, designed the portfolio builder UI and category search pages UI. Reviewed existing rank order and developed new search rank order approach.</li>'
                         '\n<li>Biomedical Imaging - Developed a semi-automatic image mosaic program based on SIFT algorithm (using Matlab)</li>\n</ul>\n</div>',
                         projects_section(['CancerDetector.com, New Jersey, USA - Project manager, codified the assessment and mapped '
                         'it to the CancerDetector ontology. Member of the UI design team, designed the portfolio '
                         'builder UI and category search pages UI. Reviewed existing rank order and developed new '
                         'search rank order approach.', 'Biomedical Imaging - Developed a semi-automatic image mosaic '
                                                        'program based on SIFT algorithm (using Matlab)']))

        #test when pulling from load_txt_file
        self.assertEqual('<div>\n<h2>Projects</h2>\n<ul>\n<li>CancerDetector.com, New Jersey, USA - Project manager, codified the assessment and mapped it to the CancerDetector ontology. '
                         'Member of the UI design team, designed the portfolio builder UI and category search pages UI. Reviewed existing rank order and developed new search rank order approach.</li>'
                         '\n<li>Biomedical Imaging - Developed a semi-automatic image mosaic program based on SIFT algorithm (using Matlab)</li>\n</ul>\n</div>',
                         projects_section(get_projects(load_txt_file('resume.txt'))))


    def test_courses_section(self):

        #test the courses section when input is written
        self.assertEqual(('<div>\n<h3>Courses</h3>\n<span>Programming Languages and Techniques, Biomedical image analysis, Software Engineering</span>\n</div>'),
                         courses_section(['Programming Languages and Techniques', 'Biomedical image analysis', 'Software Engineering']))

        #test courses section when the input is pulled from load_txt_file
        self.assertEqual(('<div>\n<h3>Courses</h3>\n<span>Programming Languages and Techniques, Biomedical image analysis, Software Engineering</span>\n</div>'),
                         courses_section(get_courses(load_txt_file('resume.txt'))))



if __name__ == '__main__':
    unittest.main()