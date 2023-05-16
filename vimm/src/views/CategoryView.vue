<template>
    <div class="page-category">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h2 class="is-size-2 has-text-centered">{{ category.name }}</h2>
            </div>

            <div class="column is-3" v-for="product in category.products" :key="product.id" :product="product">
                <ProductBox :product="product" />
            </div>
        </div>
    </div>
</template>
<script>
import ProductBox from '@/components/ProductBox.vue'
import axios from 'axios'
import { toast } from 'bulma-toast'

export default {
    name: "CategoryView",
    components: { ProductBox },
    data() {
        return {
            category: {
                products: [],
            }
        };
    },
    mounted() {
        this.getCategory();
    },
    watch: {
        $route(to, from) {
            if (to.name === 'category') {
                this.getCategory()
            }
        }
    },
    methods: {
        async getCategory() {
            this.$store.commit("setIsLoading", true);
            const category_slug = this.$route.params.category_slug;
            await axios.get(`api/v1/products/${category_slug}`)
                .then(response => {
                    this.category = response.data;
                    document.title = `Vimm | ${this.category.name}`;
                })
                .catch(error => {
                    console.log(error.message);
                    toast({
                        message: `Something went wrong.`,
                        type: "is-danger",
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: "bottom-right",
                    });
                });
            this.$store.commit("setIsLoading", false);
        }
    },
}
</script>