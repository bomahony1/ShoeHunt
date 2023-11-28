class NikeController < ApplicationController
    def index
      @nike_products = Nike.all
    end
end