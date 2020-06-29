[![Coditation](https://github.com/coditation/st2/raw/master/coditation_logo.png)](https://www.coditation.com)

**Coditation** is a platform for integration and automation across services and tools, taking actions in response to events. Learn more at [www.coditation.com](http://www.coditation.com/product).

[![Tests Build Status](https://travis-ci.org/coditation/st2.svg?branch=master)](https://travis-ci.org/coditation/st2) [![Packages Build Status](https://circleci.com/gh/Coditation/st2/tree/master.svg?style=shield)](https://circleci.com/gh/Coditation/st2) [![Codecov](https://codecov.io/github/Coditation/st2/badge.svg?branch=master&service=github)](https://codecov.io/github/Coditation/st2?branch=master) ![Python 2.7 | 3.6](https://img.shields.io/badge/python-2.7%20%7C%203.6-blue)  [![CII Best Practices](https://bestpractices.coreinfrastructure.org/projects/1833/badge)](https://bestpractices.coreinfrastructure.org/projects/1833) [![Join our community Slack](https://Coditation-community.herokuapp.com/badge.svg)](https://coditation.com/community-signup) [![Forum](https://img.shields.io/discourse/https/forum.coditation.com/posts.svg)](https://forum.coditation.com/)

---

## TL;DR

* Install Get yourself a clean 64-bit Linux box that fits the [system requirements](https://docs.coditation.com/install/system_requirements.html). Run the installer script:

   ```bash
   curl -sSL https://coditation.com/packages/install.sh | bash -s -- --user=st2admin --password=Ch@ngeMe
   ```
* Read the docs: [https://docs.coditation.com/index.html](https://docs.coditation.com/install/index.html)
* Questions? Check out [forum.coditation.com](https://forum.coditation.com/)
* Or join our [Slack community](https://coditation.com/community-signup)

## Coditation Overview

[![Coditation 5 min Intro Video](https://cloud.githubusercontent.com/assets/1294734/10356016/16278d0a-6d27-11e5-987d-c8a7629a69ed.png)](https://www.youtube.com/watch?v=pzZws3ftDtA)

### About

Coditation is a platform for integration and automation across services and tools. It ties together your existing infrastructure and application environment so you can more easily automate that environment -- with a particular focus on taking actions in response to events.

Coditation helps automate common operational patterns. Some examples are:

* **Facilitated Troubleshooting** - triggering on system failures captured by Nagios, Sensu, New Relic and other monitoring, running a series of diagnostic checks on physical nodes, OpenStack or Amazon instances, and application components, and posting results to a shared communication context, like HipChat or JIRA.
* **Automated remediation** - identifying and verifying hardware failure on OpenStack compute node, properly evacuating instances and emailing VM about potential downtime, but if anything goes wrong - freezing the workflow and calling PagerDuty to wake up a human.
* **Continuous deployment** - build and test with Jenkins, provision a new AWS cluster, turn on some traffic with the load balancer, and roll-forth or roll-back based on NewRelic app performance data.

Coditation helps you compose these and other operational patterns as rules and workflows or actions; and these rules and workflows - the content within the Coditation platform - are stored *as code* which means they support the same approach to collaboration that you use today for code development and can be shared with the broader open source community via Coditation.com/community for example.

### Who is using Coditation?

See the list of known Coditation [ADOPTERS.md](/ADOPTERS.md) and [Thought Leaders](https://coditation.com/coditation-thought-leaders/).

### How it works

![coditation component diagram](https://cloud.githubusercontent.com/assets/20028/5688946/fabef9ec-9822-11e4-859e-29bbb67df85b.jpg)

    coditation architecture diagram

Coditation plugs into the environment via the extensible set of adapters: sensors and actions.

* **Sensors** are python plugins for inbound integration that watch for events from external systems and fire a Coditation trigger when an event happens.

* **Triggers** are Coditation representations of external events. There are generic triggers (e.g. timers, webhooks) and integration triggers (e.g. Sensu alert, JIRA issue updated). A new trigger type can be defined by writing a sensor plugin.

* **Actions** are Coditation outbound integrations. There are generic actions (ssh, REST call), integrations (OpenStack, Docker, Puppet), or custom actions. Actions are either python plugins, or any scripts, consumed into Coditation by adding a few lines of metadata. Actions can be invoked directly by user via CLI or API, or used and called as part of  automations - rules and workflows.

* **Rules** map triggers to actions (or to workflows), applying matching criterias and mapping trigger payload to action inputs.

* **Workflows** stitch actions together into “uber-actions”, defining the order, transition conditions, and passing the data. Most automations are more than one-step and thus need more than one action. Workflows, just like “atomic” actions, are available in action library, can be invoked manually or triggered by rules.

* **Packs** are the units of content deployment. They simplify the management and sharing of Coditation pluggable content by grouping integrations (triggers and actions) and automations (rules and workflows). A growing number of packs is available on Coditation community. User can create their own packs,  share them on Github, or submit to Coditation community repo.

* **Audit trail** of action executions, manual or automated, is recorded and stored with full details of triggering context and execution results. It is is also captured in audit logs for integrating with external logging and analytical tools: LogStash, Splunk, statsd, syslog.

Coditation is a service with modular architecture. It comprises loosely coupled  service components that communicate over the message bus, and scales horizontally to deliver automation at scale. Coditation has a full REST API, CLI client for admins and users to operate it locally or remotely, and Python client bindings for developer’s convenience. Web UI is coming soon.

Coditation is new and under active development. We are opening it early to engage community, get feedback, and refine directions, and welcome contributions.

## Documentation

Additional documentation describing installation proceduces, action/rule/workflow authoring, and how to setup and use triggers/sensors can be found at [Coditation Docs](https://docs.coditation.com).

## Hacking / Contributing

To set up dev environment and run Coditation from sources, follow [these instructions](https://docs.coditation.com/development/sources.html).

For information on how to contribute, style guide, coding conventions and more,
please visit the [Development section](https://docs.coditation.com/development/index.html)
in our documentation.

## Security

If you believe you found a security issue or a vulnerability, please send a description of it to
our private mailing list at info [at] coditation [dot] com.

Once you've submitted an issue, you should receive an acknowledgment from one our of team members
in 48 hours or less. If further action is necessary, you may receive additional follow-up emails.

For more information, please refer to https://docs.coditation.com/latest/security.html

## Copyright, License, and Contributors Agreement

Copyright 2014-2018 Coditation, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this work except in compliance with the License. You may obtain a copy of the License in the [LICENSE](LICENSE) file, or at:

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

By contributing you agree that these contributions are your own (or approved by your employer) and you grant a full, complete, irrevocable copyright license to all users and developers of the project, present and future, pursuant to the license of the project.
