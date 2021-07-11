<template>
  <div>
    <div>
      <v-layout align-center justify-center class="mb-4">
        <v-btn color="secondary"
        @click="isShowingAddWeight = true"
          >Add Entry</v-btn
        >
      </v-layout>
    </div>

    <v-card>
       
      <v-data-table
        :headers="headers"
        :items="weights"
        :items-per-page="15"
        class="elevation-1"
      >
        <template v-slot:item.timestamp="{ item }">
          <span>{{ item.timestamp | formatDate }}</span>
        </template>
        <template v-slot:item.weight="{ item }">
          <span>
            {{item.value}} lbs
          </span>
        </template>

        <template v-slot:item.actions="{ item }">
            <v-btn
              class="mx-2 trashcan"
              fab
              dark
              x-small
              color="gray"
              @click="editWeight(item)"
            >
              <v-icon dark>
                mdi-pencil
              </v-icon>
            </v-btn>

          <v-btn
              class="mx-2 trashcan"
              fab
              dark
              x-small
              color="red"
              @click="removeWeight(item.id)"
            >
              <v-icon dark>
                mdi-delete
              </v-icon>
            </v-btn>
        </template>
        <template v-slot:no-data>
          No feeds yet
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="isShowingAddWeight" max-width="400px">
      <add-weight @closeDialog="isShowingAddWeight = false"></add-weight>
    </v-dialog>

    <v-dialog v-model="isShowingEditWeight" max-width="400px">
      <edit-weight :weight="selectedWeight" @closeDialog="isShowingEditWeight = false"></edit-weight>
    </v-dialog>
  </div>
</template>

<script>
import AddWeight from './AddWeight.vue';
import EditWeight from './EditWeight.vue';
export default {
  components: { AddWeight, EditWeight },
  name: "PetWeights",

  data: () => ({
    weights: [],
    intervalId: "",
    isShowingAddWeight: false,
    isShowingEditWeight: false,
    
    headers: [
      {
        text: "Timestamp",
        align: "start",
        sortable: true,
        value: "timestamp",
      },
      { text: "Weight", value: "value" },
      { text: "", value: "actions" },
    ],
  }),
  mounted() {
    this.fetchData();
    this.intervalId = setInterval(this.fetchData, 6000);
  },
  destroyed() {
    window.clearInterval(this.intervalId);
  },
  methods: {
    authenticate() {
      if (this.username != "" || this.password != "") {
        if (this.username == "drew" && this.password == "millie") {
          this.$emit("authEvent", true);
        } else {
          this.errorMessage = "Incorrect username or password";
        }
      } else {
        this.errorMessage = "Username and password cannot be blank";
      }
    },
    fetchData() {
      let apiUrl = process.env.VUE_APP_BACKEND_URL + "?action=all_pet_weights";
      this.axios.get(apiUrl, {}).then((response) => {
        this.weights = response.data;
      });
    },
    editWeight(item) {
      this.selectedWeight = item;
      this.isShowingEditWeight = true;
    },
    removeWeight(id) {
      let body = "action=delete_pet_weight&id=" + id;
      let apiUrl = process.env.VUE_APP_BACKEND_URL;
      this.axios.post(apiUrl, body).then((response) => {
        this.scheduleResult = response.data;
      });

      var self = this;
      setTimeout(() => {
        self.fetchData();
      }, 600);
    }
  },
};
</script>



<style scoped>
.trashcan i {
  color: white !important;
}
</style>