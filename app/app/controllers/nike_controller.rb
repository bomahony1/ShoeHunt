class NikeController < ApplicationController
    def index
      @nike_products = Nike.all
    end

    def nikeshoes
      @nike_products = Nike.all
    end
end