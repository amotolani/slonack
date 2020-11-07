from slack import slackit
from pullrequestprofile import PullRequestProfile
from htmlgenerator import HTMLGenerator
import argparse

def main():

    parser = argparse.ArgumentParser(description='Collect data from cli')
    parser.add_argument("pullrequest", type=int, help='PullRequest Key')
    parser.add_argument("projectkey", type=str, help='SonarCloud Project Key')
    parser.add_argument("channel", type=str, help='Slack Channel')
    parser.add_argument("sonar_token", type=str, help='Sonar Cloud Authentication')
    parser.add_argument("slack_token", type=str, help='Slack APP Authentication')

    args = parser.parse_args()

    pullrequest = PullRequestProfile(authorization=args.sonar_token, pullrequest=args.pullrequest, projectkey=args.projectkey)
    gate_status = pullrequest.gate_status()

    if gate_status[0]['status'] == 'OK':
        status = 'PASSED'
        status_emoji = ':thumbsup:'
        color = '#00ff00'
    else:
        status = 'FAILED'
        status_emoji= ':thumbsdown:'
        color = '#ff0000'

    message_load=[
		{
            "color": "{}".format(color),
			"blocks": [
				{
					"type": "divider"
				},
				{
					"type": "header",
					"text": {
						"type": "plain_text",
						"text": "SonarCloud Quality Gate Status :alert: "
					}
				},
				{
					"type": "section",
					"text": {
						"type": "plain_text",
						"text": "{}  {}".format(status, status_emoji)
					}
				},
				{
					"type": "section",
					"text": {
						"type": "plain_text",
						"text": "SonarCloud Project: {}".format(args.projectkey)
					}
				},
				{
					"type": "context",
					"elements": [
						{
							"type": "plain_text",
							"text": "Your current measures for Pull Request #{}".format(args.pullrequest)
						}
					]
				},                				
                {
					"type": "divider"
				},				
				{
					"type": "divider"
				},
				{
					"type": "divider"
				},
				{
					"type": "header",
					"text": {
						"type": "plain_text",
						"text": "@NIBSSDevops :sunglasses:"
					}
				}
			]
		}
	]

    for i in range(1, len(gate_status)):
        gate_condition = gate_status[i]
        measure = gate_condition.get('metric')
        threshold = gate_condition.get('threshold')
        value = gate_condition.get('value', 'N/A')
        operator = gate_condition.get('operator')


        # Logic to determine the emoji to display on each measure
        if value != 'N/A':
            if operator == 'LT':
                operator = 'less than'
                if float(value) < float(threshold) :
                    measure_emoji = ':x:'
                else:
                    measure_emoji = ':white_check_mark:'
            if operator == 'GT':
                operator = 'greater than'
                if float(value) > float(threshold) :
                    measure_emoji = ':x:'
                else:
                    measure_emoji = ':white_check_mark:'
        else:
            measure_emoji = ':man-shrugging:'

        # Format the Measure String and Round off the value to 3 digits
        m = measure.split('_')
        measure = ' '.join(m).title()
        value = int(float(value))

        # Construct the Message blocks for each measure
        measure_condition= {
                            "type": "section",
                            "text": {
                                "type": "plain_text",
                                "text": "{} : {}  {}".format(measure, value, measure_emoji)
                            }
                        }

        measure_criteria={
                            "type": "context",
                            "elements": [
                                {
                                    "type": "plain_text",
                                    "text": "#Must not be {} {}".format(operator, threshold)
                                }
                            ]
                        }
        
        message_load[0]['blocks'].insert(6, measure_criteria)
        message_load[0]['blocks'].insert(6, measure_condition)

    #Get all Open issuses
    issues = pullrequest.issues(status='OPEN')

    #Select reportable information on  Open Issues.
    report_data = pullrequest.issues_info(issues)
    report_title = 'Open Issues:  PullRequest #' + str(args.pullrequest) + ' - Project: ' + str(args.projectkey)

    if len(report_data) != 0:
        HTMLGenerator().create_report(report_title=report_title, report_data=report_data)
        post = slackit(channel=args.channel, authorization=args.slack_token)
        post_response = post.post_message(attachments=message_load)
        thread_ts = post_response['ts']
        post.post_file(file='report.html', thread_ts=thread_ts)

    else:
        post = slackit(channel=args.channel, authorization=args.slack_token)
        post.post_message(attachments=message_load)


if __name__ == "__main__":
    main()