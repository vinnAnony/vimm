<template>
    <div class="page-sign-up">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title has-text-centered">Sign up</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Username</label>
                        <div class="control">
                            <input type="text" class="input" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password">
                        </div>
                    </div>

                    <div class="field">
                        <label>Confirm password</label>
                        <div class="control">
                            <input type="password" class="input" v-model="password_confirmation">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control has-text-centered">
                            <button class="button is-dark">Sign Up</button>
                        </div>
                    </div>

                    <hr>

                    Already have an account? <router-link to="/login">Log In</router-link>
                </form>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
import { toast } from 'bulma-toast'

export default {
    name: "SignUpView",
    data() {
        return {
            username: '',
            password: '',
            password_confirmation: '',
            errors: [],
        }
    },
    mounted() {
        document.title = `Vimm | Sign Up`
    },
    methods: {
        submitForm() {
            this.errors = []

            if (this.username === '') {
                this.errors.push('Kindly provide a username')
            }
            if (this.password === '') {
                this.errors.push('Kindly provide a password')
            }
            if (this.password_confirmation === '') {
                this.errors.push('Confirm your password')
            }
            if (this.password !== this.password_confirmation) {
                this.errors.push("The password doesn't match")
            }

            if (!this.errors.length) {
                const formData = {
                    username: this.username,
                    password: this.password,
                }

                axios.post('/api/v1/users/', formData)
                    .then(response => {
                        toast({
                            message: `Account created successfully, please login.`,
                            type: 'is-success',
                            dismissible: true,
                            pauseOnHover: true,
                            duration: 2000,
                            position: 'bottom-right',
                        })

                        this.$router.push('/login')
                    })
                    .catch(error => {
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }

                            console.log(JSON.stringify(error.response.data))
                        } else if (error.message) {
                            this.errors.push('Something went wrong. Please try again')

                            console.log(JSON.stringify(error))
                        }
                    })
            }
        }
    },
}
</script>
<style></style>