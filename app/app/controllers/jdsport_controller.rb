class JdsportController < ApplicationController
    def jdsportshoes
        @jdsportproduct = Jdsport.all
    end
end