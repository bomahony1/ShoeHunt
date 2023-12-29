# app/controllers/products_controller.rb
class ProductsController < ApplicationController
  def show
    @nike_products = Nike.all
    @jdsport_products = Jdsport.all
    @all_products = [@nike_products, @jdsport_products].flatten

    # Find the product with the specified id
    @product = @all_products.find { |product| product.id == params[:id].to_i }

    # Additional logic here if @product needs further customization
  end
end
