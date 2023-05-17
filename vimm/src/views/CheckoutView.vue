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

            if (!this.errors.length) {
                this.$store.commit("setIsLoading", true);

                // TODO: Trigger STK Push and get mpesa_code from backend
                this.mpesaPaymentHandler('MP3SAC0D3')
            }
        },
        async mpesaPaymentHandler(mpesa_code) {
            const items = []

            for (let i = 0; i < this.cart.items.length; i++) {
                const item = this.cart.items[i];
                const obj = {
                    product: item.product.id,
                    quantity: item.quantity,
                    price: item.product.price * item.quantity,
                }

                items.push(obj)

            }
            const formData = {
                'first_name': this.first_name,
                'last_name': this.last_name,
                'email': this.email,
                'phone': this.phone,
                'address': this.address,
                'place': this.place,
                'items': items,
                'mpesa_code': mpesa_code,
            }

            await axios.post('/api/v1/checkout/', formData)
                .then(response => {
                    this.$store.commit("clearCart")
                    this.$router.push('/cart/success')
                })
                .catch(error => {
                    if (error.response.status === 500) {
                        this.errors.push('Something went wrong. Please try again')
                    } else {
                        if (error.response) {
                            for (const property in error.response.data) {
                                this.errors.push(`${property}: ${error.response.data[property]}`)
                            }

                            console.log(JSON.stringify(error.response.data))
                        } else if (error.message) {
                            this.errors.push('Something went wrong. Please try again')

                            console.log(JSON.stringify(error))
                        }
                    }

                })

            this.$store.commit("setIsLoading", false);
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