class RootController < ApplicationController
    def index
        @nike_products = Nike.all
        @jdsport_products = Jdsport.all
        @all_products = [@nike_products, @jdsport_products].flatten
    end

end