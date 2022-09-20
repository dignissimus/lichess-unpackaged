#!/usr/bin/env perl

my $MAX_GAMES = 100000;

while ($MAX_GAMES--) {
    // while (<> ne "\n");
    (reverse scalar <>) =~ /[A-Za-z]+ \.{1,3}(\d+)/;
    print scalar reverse $1;
    print "\n";
    <>;
    last if eof;
}
