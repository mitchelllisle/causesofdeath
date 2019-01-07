import pandas as pd
# import os
# os.chdir("/Users/mitchell/Documents/projects/causesofdeath")


def readData():
    return pd.read_csv("core/data/public/causesofdeath.csv")


def autocomplete_categories():
    causes = readData()
    choices = [tuple([x, x]) for x in causes['chapter'].unique()]
    return choices


def get_category_detail(category):
    category_details = {
        "Mental and behavioural disorders": """The Australian Bureau of Statistics treats this category as such: 'People of all ages can develop symptoms and behaviours that are distressing to themselves or others, and interfere with their social functioning and capacity to negotiate daily life. These symptoms and behaviours may require treatment, rehabilitation, or even hospitalisation. A diverse range of social, environmental, biological and psychological factors can impact on an individual’s mental health.'
        <br><br>
        In this study, dying from mental illness and behaviour disorders include dying from a depressive episode, dementia, substance abuse and other causes that are psychological in nature.
        <br><br>
        For the most part, we have seen a steady increase since 2008 in the number of deaths from these issues. Although the increase each year has been steady, dementia and symptomatic (other wise known as ‘organic’) mental disorders have seen the most increase from 2008 to 2017."""
    }
    return category_details.get(category, None)
