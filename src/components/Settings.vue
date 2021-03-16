<template>
  <v-container>
    <v-card class="mx-auto">
      <v-card-title>
        Feeder Settings
      </v-card-title>
      <v-card-text>
        <v-row>
          <v-col>
            <v-text-field
              label="Pet name"
              placeholder=""
              v-model="settings.petName"
              outlined
            ></v-text-field>
          </v-col>
          <v-col>
            <v-layout align-center justify-center>
              <v-checkbox
                v-model="settings.twoBowls"
                :label="`Two Bowls`"
              ></v-checkbox>
            </v-layout>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field
              label="Username"
              placeholder=""
              v-model="settings.username"
              outlined
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              label="Password"
              placeholder=""
              v-model="settings.password"
              outlined
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field
              label="Device name"
              placeholder=""
              v-model="settings.feederName"
              outlined
            ></v-text-field>
          </v-col>
          <v-col>
            <v-text-field
              label="1 Cup Duration (seconds)"
              placeholder=""
              type="number"
              v-model="settings.cupDuration"
              outlined
            ></v-text-field>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <v-layout align-center justify-center>
              <v-switch
                v-model="settings.isUsingAlexa"
                label="Alexa"
              ></v-switch>
            </v-layout>
            <v-text-field
              v-if="settings.isUsingAlexa"
              label="Sincric API Key"
              placeholder=""
              v-model="settings.sinricAPI"
              outlined
            ></v-text-field>
            <v-text-field
              v-if="settings.isUsingAlexa"
              label="Sincric Device ID"
              placeholder=""
              v-model="settings.sinricDeviceId"
              outlined
            ></v-text-field>
            <v-select
              v-if="settings.isUsingAlexa"
              v-model="settings.defaultFeedAmount"
              :items="amounts"
              type="number"
              label="Alexa Default Feed Amount (cups)"
              hint="Cups"
              persistent-hint
              outlined
            ></v-select>
          </v-col>
          <v-col>
            <v-layout align-center justify-center>
              <v-switch
                v-model="settings.isUsingScale"
                label="Scale"
              ></v-switch>
            </v-layout>
            <v-text-field
              v-if="settings.isUsingScale"
              label="Full Bowl Weight (g)"
              placeholder=""
              type="number"
              v-model="settings.fullBowlWeight"
              outlined
            ></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-layout align-center justify-center class="pt-2">
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    rounded
                    color="secondary"
                    @click="resetScale"
                    :disabled="isUpdating"
                    v-bind="attrs"
                    v-on="on"
                  >
                    Reset Scale
                  </v-btn>
                </template>
                <span>Please empty bowl before resetting the scale</span>
              </v-tooltip>
            </v-layout>
          </v-col>
          <v-col>
            <v-layout align-center justify-center class="pt-2">
              <v-btn
                rounded
                color="secondary"
                @click="resetAlexa"
                :disabled="isUpdating"
              >
                Reset Alexa
              </v-btn>
            </v-layout>
          </v-col>
          <v-col>
            <v-layout align-center justify-center class="pt-2">
              <v-btn
                rounded
                color="secondary"
                @click="updateSettings"
                :disabled="isUpdating || !fieldsHaveChanged"
              >
                Update
              </v-btn>
            </v-layout>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-layout align-center justify-center>
          <p>{{ feedResult }}</p>
        </v-layout>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script>
import _ from "lodash";

export default {
  name: "Settings",

  data: () => ({
    feederId: 1,
    amount: "1",
    feedResult: "",
    amounts: [".5", "1", "1.5", "2", "2.5", "3"],
    tempSettings: {},
    settings: {
      petName: "",
      twoBowls: false,
      username: "admin",
      password: "admin",
      feederName: "",
      defaultFeedAmount: 1,
      fullBowlWeight: 0.0,
      cupDuration: 3.0,
      isUsingScale: false,
      isUsingAlexa: false,
      sinricAPI: "",
      sinricDeviceId: "",
    },
    isUpdating: false,
  }),
  computed: {
    fieldsHaveChanged() {
      let fieldsHaveChanged = false;
      if (this.tempSettings != {}) {
        fieldsHaveChanged = !_.isEqual(this.tempSettings, this.settings);
      } else {
        fieldsHaveChanged = true;
      }

      return fieldsHaveChanged;
    },
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      let apiUrl =
        process.env.VUE_APP_BACKEND_URL +
        "?action=feeder_settings&id=" +
        this.feederId;
      this.axios.get(apiUrl, {}).then((response) => {
        this.settings = JSON.parse(response.data[0].preferences);
        this.tempSettings = _.cloneDeep(this.settings);
      });
    },
    updateSettings() {
      this.isUpdating = true;
      let body =
        "action=update_preferences&preferences=" +
        JSON.stringify(this.settings);
      let apiUrl = process.env.VUE_APP_BACKEND_URL;
      this.axios.post(apiUrl, body).then((response) => {
        this.isUpdating = false;
        this.fetchData();
      });
    },
    resetScale() {
      this.isUpdating = true;
      let body = "action=reset_scale";
      let apiUrl = process.env.VUE_APP_BACKEND_URL;
      this.axios.post(apiUrl, body).then((response) => {
        this.isUpdating = false;
      });
    },
    resetAlexa() {
      this.isUpdating = true;
      let body = "action=reset_alexa";
      let apiUrl = process.env.VUE_APP_BACKEND_URL;
      this.axios.post(apiUrl, body).then((response) => {
        this.isUpdating = false;
      });
    },
  },
};
</script>
