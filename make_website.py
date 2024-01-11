def surround_block(tag, text):
    '''
    Surrounds the given text with the given html tag and returns the string.
    :param tag: the tag used to surround text
    :param text: passed in text to be tagged
    :return: the complete formatted string
    '''

    tagged_block = ('<' + tag + '>' + text + '</' + tag + '>')

    return tagged_block


def create_email_link(email_address):
    """
    Creates an email link with the given email_address.
    To cut down on spammers harvesting the email address from the webpage,
    displays the email address with [aT] instead of @.

    Example: Given the email address: lbrandon@wharton.upenn.edu
    Generates the email link: <a href="mailto:lbrandon@wharton.upenn.edu">lbrandon[aT]wharton.upenn.edu</a>

    Note: If, for some reason the email address does not contain @,
    use the email address as is and don't replace anything.
    """

    if '@' in email_address:
        aT_email = email_address.replace('@', '[aT]')
    else:
        aT_email = email_address

    email_html_code = ('<a href="mailto:' + email_address + '">' + aT_email + '</a>')

    return email_html_code



def load_txt_file(txt_input_file):
    '''
    This function opens the given file, reads each line and strips whitespace/deletes empty lines, and creates a list
    of the lines in the file
    :param txt_input_file: given file to be read
    :return: a list of each line in the file
    '''

    txt_name = open(txt_input_file, 'r')

    lines = txt_name.readlines()

    #this list will be appended with non-empty lines
    new_lines = []

    for line in lines:
        #strip the leading and trailing whitespace form each line
        new_line = line.strip()
        #if the line is empty, don't add it to new_lines list
        if new_line == '':
            continue
        else:
            #if the line isn't empty, append to the new_lines list
            new_lines.append(new_line)

    txt_name.close()

    #return this new list to be used in the other functions
    return new_lines

def get_name(name_line):
    '''
    takes in the name line, which we know to be the first line, and returns the name or 'invalid name'
    :param name_line: the first line of the txt file
    :return: the given name as a string
    '''

    #strip the anme if any whitespace. This should already be done when the file is read load_txt_file but double check
    name = name_line.strip()

    if name[0].isupper():
        name = name
    else:
        name = 'Invalid Name'

    return name

def get_email(lines):
    '''
    takes in all the lines of the txt file and searches for the @ symbol. Returns that line as the email if found
    :param lines: all lines fo the given txt file
    :return: a string of the email (if found)
    '''

    #if an email is not found, this empty line will be returned instead
    email = ''

    # iterate through each line to look for the email @ symbol
    for line in lines:
        if '@' in line:

            # if @ is found, iterate through each letter to look for valid contingencies
            for l in line:

                #if a number is found, then break out of the for loop
                if l.isnumeric():
                    #I have to reassign email back to '' because the end of these nested loops would have been reached if there were any letters before the number
                    email = ''
                    break

                else:
                    #using slices to check last 4 chars of the list
                    if line[-4:] == '.com' or line[-4:] == '.edu':

                        for l in line[(line.index('@')):]:

                            #ensure there's a lowercase letter after the @
                            if l.islower():

                                #if there is a lowercase after the @, then we've satified all conditions! email = line
                                email = line
                                break

                            else:
                                continue
                    else:
                        break
            else:
                break

    return email

def get_courses(lines):
    '''
    Extracts the course string line from the list of strings that was extracted from the txt file.
    Removes the unwanted weird punctuation and whitespace and returns a list of courses
    :param lines: this is a list of all the lines in the txt file
    :return: a list with the courses (no whitespace or odd characters)
    '''

    #call locate_line to get the index of the line with courses
    course_line_index = locate_line(lines, 'Courses')

    #First step in isolating the courses is to remove 'Courses' from the line. Find index of 'Courses'
    start_index = lines[course_line_index].index('Courses')

    #slice everything before the start_index+length of courses
    course_line = lines[course_line_index][start_index + len('Courses'):]


    #replace all whitespace and random punctuation before the first letter with an empty place
    for l in course_line:
        if l.isalpha() == False:
            course_line = course_line.replace(l, '', 1)
        else:
            #once a letter is found, break from this loop because that means the course list is beginning
            break

    #create a list from the string
    list_of_courses = course_line.split(',')

    new_course_list = []

    for course in list_of_courses:
        #lists are immutable, so we need to create a new_course that is stripped
        new_course = course.strip()

        #add the new course to the new_course_list
        new_course_list.append(new_course)

    return new_course_list


def get_projects(lines):
    '''
    this function takes in all lines and creates a slice of just the projects using the index of the project
    line and project end indicator (----------)
    :param lines: all lines in the txt file
    :return: a list of string of all the projects
    '''

    #locate the index for the project line
    project_line = locate_line(lines, 'Projects')

    # locate the index for the line indicating the end of projects
    project_ending_line = locate_line(lines, '----------')

    #slice the lines list to get a new list with only the lines between project_line and project_ending_line
    project_list = lines[project_line+1:project_ending_line]

    return project_list

def locate_line(lines, line_identifier):
    '''
    Locate and return the specific line that line_identifier exists on
    :param line_identifier: a string that will be searched for in all lines
    :param lines: list of all lines from the txt file
    :return: the index of the specific line that the identifier exists on
    '''

    #course_line is initially set to empty, in case the line we're looking for doesn't exist
    line_index = None

    # search for the line with 'Courses.' once found, break out of for loop
    for line in lines:
        if line_identifier in line:
            course_line = line
            line_index = lines.index(course_line)
            break

    #line_index = lines.index(course_line)

    return line_index


def load_html_template():
    '''
    loads the html template and removes the last two lines
    :return: a list of all the lines in the template minus the last two
    '''

    template = open('resume_template.html', 'r')

    #read the templates lists into a list
    template_lines = template.readlines()

    #print(template_lines)

    #remove the last two items, which are '</body>\n' and '</html>\n'
    template_lines.pop()
    template_lines.pop()

    template.close()

    return template_lines


def basic_info_section(name, email):
    '''
    creates the html formatted section for basic info (name and email)
    :param name: the string name that was extracted from the txt file
    :param email: the string email that was extracted from the txt file
    :return: an html formatted string that has the basic info
    '''

    #surround the html formatted name and email with a div black. This single (long) line creates the whole basic info section
    basic_info_section = surround_block('div', '\n' + surround_block('h1', name) + '\n'
                                        + surround_block('p', 'Email: ' + create_email_link(email)) + '\n')

    return basic_info_section


def projects_section(projects):
    '''
    this function creates a string with the html language to write the project section
    :param projects: takes in a list of the txt file projects
    :return: a string in html format
    '''

    project_header = surround_block('h2', 'Projects')

    html_project_list = []

    #surround every project in the project list with the correct html formatting
    for project in projects:
        html_project = surround_block('li', project)
        html_project_list.append(html_project)

    #combine the list of html formatted projects into a single string with newlines for formatting
    projects_li = '\n'.join(html_project_list)

    projects_ul = surround_block('ul', '\n' + projects_li + '\n')

    #this could all be done on one line but i felt it was more readable to seperate each surround_block() step
    projects_section = surround_block('div', '\n' + project_header + '\n' + projects_ul + '\n')

    return projects_section


def courses_section(courses):
    '''
    turns the list of courses into an html formatted string
    :param courses: a list of courses from the html file
    :return: an html formatted string with all the courses in proper hmtl format
    '''

    #the \n characters ensure the correct format when we use this section in the html file
    # .join method used to combine the list of courses into a string
    courses_section = surround_block('div', '\n' + surround_block('h3', 'Courses') + '\n'
                                     + surround_block('span', ', '.join(courses)) + '\n')

    return courses_section


def write_to_html(html_output_file, html_template_lines, name, email, projects, courses):
    '''
    this function opens the html output file for writing and first writes the template lines. It takes all
    the html formatted sections and appends them to the html output file.
    :param html_output_file: the html file that will be written to for each resume txt file
    :param html_template_lines: the html template lines we created in load_html_file
    :param name: string name from the txt file
    :param email: string email from the txt file
    :param projects: list of projects from the txt file
    :param courses: list of courses from the txt file
    :return: nothing, just writes to the file
    '''

    stream = open(html_output_file, 'w')

    #write all the template lines to the html output file
    stream.writelines(html_template_lines)

    #write the needed div lines provided in the assignment writeup
    stream.write('<div id="page-wrap">\n')

    #various \n spaces to ensure correct and clean format
    stream.write('\n')

    stream.write(basic_info_section(name, email))

    stream.write('\n\n')

    stream.write(projects_section(projects))

    stream.write('\n\n')

    stream.write(courses_section(courses))

    #ending lines from the assingment writeup
    stream.write('\n\n</div>\n</body>\n</html>')

    stream.close()



def generate_html(txt_input_file, html_output_file):
    '''
    Loads given txt_input_file,
    gets the name, email address, list of projects, and list of courses,
    then writes the info to the given html_output_file.
    :param txt_input_file: the file to gather data from
    :param html_output_file: the html file to write to
    :return: nothing, just performs functions
    '''

    # lines is a list where each element is a line in the code
    lines = load_txt_file(txt_input_file)

    # name will be a string
    name = get_name(lines[0])

    # email will be a string
    email = get_email(lines)

    # courses will be a list
    courses = get_courses(lines)

    # projects will be a list
    projects = get_projects(lines)

    # will be a list of all html template lines
    html_template_lines = load_html_template()

    #write to the given html file
    write_to_html(html_output_file, html_template_lines, name, email, projects, courses)


def main():

    # DO NOT REMOVE OR UPDATE THIS CODE
    # generate resume.html file from provided sample resume.txt
    generate_html('resume.txt', 'resume.html')

    # DO NOT REMOVE OR UPDATE THIS CODE.
    # Uncomment each call to the generate_html function when you’re ready
    # to test how your program handles each additional test resume.txt file
    generate_html('TestResumes/resume_bad_name_lowercase/resume.txt', 'TestResumes/resume_bad_name_lowercase/resume.html')
    generate_html('TestResumes/resume_courses_w_whitespace/resume.txt', 'TestResumes/resume_courses_w_whitespace/resume.html')
    generate_html('TestResumes/resume_courses_weird_punc/resume.txt', 'TestResumes/resume_courses_weird_punc/resume.html')
    generate_html('TestResumes/resume_projects_w_whitespace/resume.txt', 'TestResumes/resume_projects_w_whitespace/resume.html')
    generate_html('TestResumes/resume_projects_with_blanks/resume.txt', 'TestResumes/resume_projects_with_blanks/resume.html')
    generate_html('TestResumes/resume_template_email_w_whitespace/resume.txt', 'TestResumes/resume_template_email_w_whitespace/resume.html')
    generate_html('TestResumes/resume_wrong_email/resume.txt', 'TestResumes/resume_wrong_email/resume.html')

    # If you want to test additional resume files, call the generate_html function with the given .txt file
    # and desired name of output .html file

if __name__ == '__main__':
    main()