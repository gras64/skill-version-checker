# Copyright 2017 Mycroft AI, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mycroft.util
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.version import CORE_VERSION_STR


class VersionCheckerSkill(MycroftSkill):
    def __init__(self):
        super(VersionCheckerSkill, self).__init__("VersionCheckerSkill")

    def initialize(self):
        intent = IntentBuilder('CheckVersion').require('Check') \
            .require('Version').build()
        self.register_intent(intent, self.check_version)

        intent = IntentBuilder('CheckPlatformBuild').require('Check') \
            .require('PlatformBuild')
        self.register_intent(intent, self.check_platform_build)

    def check_version(self, message):
        # Report the version of mycroft-core software
        self.enclosure.deactivate_mouth_events()
        self.enclosure.mouth_text(CORE_VERSION_STR)

        self.speak_dialog('version', data={'version': CORE_VERSION_STR})

        # NOTE: intentionally sticking with this deprecated API instead
        # of mycroft.audio.wait_while_speaking() so that this skill
        # works on 0.8.15+
        mycroft.util.wait_while_speaking()
        self.enclosure.activate_mouth_events()

    def check_platform_build(self, message):
        if 'platform_build' in self.config_core['enclosure']:
            # Report the platform build (aka firmware version)
            build = self.config_core['enclosure']['platform_build']
            self.enclosure.deactivate_mouth_events()
            self.enclosure.mouth_text(build)

            self.speak_dialog('platform.build', data={'build': build})

            mycroft.util.wait_while_speaking()
            self.enclosure.activate_mouth_events()
        else:
            self.speak_dialog('platform.build.none')

    def stop(self):
        pass


def create_skill():
    return VersionCheckerSkill()
