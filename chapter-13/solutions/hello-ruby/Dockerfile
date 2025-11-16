FROM ruby:latest
WORKDIR /usr/src/app
# Copy dependency files first (for better caching)
COPY Gemfile Gemfile.lock ./
# Install bundler and gems
RUN gem install bundler && \
    bundle install --jobs 4 --retry 3
# Copy the rest of the app’s code
COPY . .
EXPOSE 4567
CMD ["bundle", "exec", "puma", "-p", "4567", "-b", "tcp://0.0.0.0"]