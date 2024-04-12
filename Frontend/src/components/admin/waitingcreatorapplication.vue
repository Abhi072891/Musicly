<template>
    <div>
      <h2>Creator Waiting Applications</h2>
      <ul>
        <li v-for="user in users" :key="user.user_id">
          {{ user.username }}
          <button @click="approve(user.user_id)">Approve</button>
          <button @click="reject(user.user_id)">Reject</button>
        </li>
      </ul>
    </div>
</template>

<script>
  export default {
    data() {
      return {
        users: [],
      };
    },
    mounted() {
      this.fetchWaitingCreators();
    },
    methods: {
      fetchWaitingCreators() {
        fetch('http://127.0.0.1:5000/creatorwaiting')
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            this.users = data;
          })
          .catch(error => {
            console.error('Error fetching creator waiting applications:', error);
          });
      },
      approve(userId) {
        if (confirm("Are you sure you want to approve this creator application?")) {
        fetch(`http://127.0.0.1:5000/creatorapprove/${userId}`)
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            console.log('Creator application approved successfully');
            // Remove the approved user from the list
            this.users = this.users.filter(user => user.user_id !== userId);
          })
          .catch(error => {
            console.error('Error approving creator application:', error);
          });
      }},
      reject(userId) {
        if (confirm("Are you sure you want to reject this creator application?")) {
        fetch(`http://127.0.0.1:5000/creatorreject/${userId}`)
          .then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            console.log('Creator application rejected successfully');
            // Remove the rejected user from the list
            this.users = this.users.filter(user => user.user_id !== userId);
          })
          .catch(error => {
            console.error('Error rejecting creator application:', error);
          });
      }},
    },
  };
</script>

<style scoped>
/* Add your custom styles here */
</style>
  