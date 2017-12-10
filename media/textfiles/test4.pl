#!/usr/bin/perl -wT
use strict;
use CGI;
use GD::Graph::pie;
my $q = new CGI;
my $graph = new GD::Graph::pie( 300, 300 );
#my @data =  read_data();
my @data = (['Paris','Frankfurt','London'],
            [7309,5322,9719] ) ;
$graph->set(
    title        => "Pie: total orders",
    transparent  => 1,
    "3d"         => 0,
);
my $gd_image = $graph->plot( \@data );
print $q->header( -type => "image/png", -expires => "-1d" );
binmode STDOUT;
print $gd_image->png;
