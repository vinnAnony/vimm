<template>
    <div class="page-checkout">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Checkout</h1>
            </div>

            <div class="column is-12 box">
                <table class="table is-fullwidth">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>Price</th>
                            <th>Quantity</th>
                            <th>Total</th>
                        </tr>
                    </thead>

                    <tbody>
                        <tr v-for="item in cart.items" v-bind:key="item.product.id">
                            <td>{{ item.product.name }}</td>
                            <td>KES {{ item.product.price }}</td>
                            <td>{{ item.quantity }}</td>
                            <td>KES {{ getItemTotal(item).toFixed(2) }}</td>
                        </tr>
                    </tbody>

                    <tfoot>
                        <tr>
                            <td colspan="2">Total</td>
                            <td>{{ cartTotalLength }}</td>
                            <td>KES {{ cartTotalPrice.toFixed(2) }}</td>
                        </tr>
                    </tfoot>
                </table>
            </div>
            <div class="column is-12 box">
                <h2 class="subtitle">Shipping details</h2>

                <p class="has-text-grey mb-4">* All fields are required</p>

                <div class="columns is-multiline">
                    <div class="column is-6">
                        <div class="field">
                            <label>First name*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="first_name">
                            </div>
                        </div>

                        <div class="field">
                            <label>Last name*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="last_name">
                            </div>
                        </div>

                        <div class="field">
                            <label>E-mail*</label>
                            <div class="control">
                                <input type="email" class="input" v-model="email">
                            </div>
                        </div>

                        <div class="field">
                            <label>Phone*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="phone">
                            </div>
                        </div>
                    </div>

                    <div class="column is-6">
                        <div class="field">
                            <label>Address*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="address">
                            </div>
                        </div>

                        <div class="field">
                            <label>Place*</label>
                            <div class="control">
                                <input type="text" class="input" v-model="place">
                            </div>
                        </div>
                    </div>
                </div>

                <div class="notification is-danger mt-4" v-if="errors.length">
                    <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                </div>

                <hr>

                <div id="card-element" class="mb-5"></div>

                <template v-if="cartTotalLength">
                    <hr>

                    <button class="button is-dark" @click="submitForm">Pay with M-PESA</button>
                </template>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios';

export default {
    name: "",
    data() {
        return {
            cart: {
                items: []
            },
            stripe: {},
            card: {},
            first_name: '',
            last_name: '',
            email: '',
            phone: '',
            address: '',
            place: '',
            errors: [],
        }
    },
    mounted() {
        this.cart = this.$store.state.cart

        document.title = `Vimm | Checkout`
    },
    methods: {
        getItemTotal(item) {
            return item.quantity * item.product.price
        },
        submitForm() {
            this.errors = []

            if (this.first_name === '') {
                this.errors.push('Kindly provide first name')
            }
            if (this.last_name === '') {
                this.errors.push('Kindly provide last name')
            }
            if (this.email === '') {
                this.errors.push('Kindly provide an email')
            }
            if (this.phone === '') {
                this.errors.push('Kindly provide a phone number')
            }
            if (this.address === '') {
                this.errors.push('Kindly provide an address')
            }
            if (this.place === '') {
                this.errors.push('The place field is required')
            }
        }
    },
    computed: {
        cartTotalLength() {
            return this.cart.items.reduce((acc, currVal) => {
                return acc += currVal.quantity;
            }, 0);
        },
        cartTotalPrice() {
            return this.cart.items.reduce((acc, currVal) => {
                return acc += currVal.product.price * currVal.quantity;
            }, 0);
        }
    },
}
</script>
<style></style>